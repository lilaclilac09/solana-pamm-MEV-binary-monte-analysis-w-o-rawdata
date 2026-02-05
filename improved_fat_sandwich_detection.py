"""
Improved Fat Sandwich Detection with Rolling Time Windows

This module implements accurate fat sandwich detection using:
1. True rolling time windows (1s, 2s, 5s, 10s)
2. Multiple verification mechanisms
3. Precise millisecond-based timing

Author: Optimized MEV Detection System
Date: 2026-02-04
"""

import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


def detect_fat_sandwich_time_window(
    trades_df,
    window_seconds=[1, 2, 5, 10],
    min_trades=5,
    max_victim_ratio=0.8,
    min_attacker_trades=2,
    verbose=True
):
    """
    Detect fat sandwich patterns using true rolling time windows.
    
    Parameters:
    -----------
    trades_df : DataFrame
        All TRADE events with columns: ['signer', 'ms_time', 'slot', 'validator', 
                                        'amm_trade', 'from_token', 'to_token']
    window_seconds : list
        Time window sizes in seconds (default: [1, 2, 5, 10])
    min_trades : int
        Minimum number of trades in window to consider (default: 5)
    max_victim_ratio : float
        Maximum victim/total ratio to avoid aggregator routing (default: 0.8)
    min_attacker_trades : int
        Minimum attacker trades (front + back) (default: 2)
    verbose : bool
        Print progress messages
    
    Returns:
    --------
    results_df : DataFrame
        Detected fat sandwich patterns with confidence scores
    stats : dict
        Detection statistics
    """
    
    if verbose:
        print("=" * 80)
        print("IMPROVED FAT SANDWICH DETECTION: Rolling Time Windows")
        print("=" * 80)
        print(f"Dataset: {len(trades_df):,} TRADE events")
        print(f"Time windows: {window_seconds} seconds")
        print(f"Min trades per window: {min_trades}")
        print(f"Max victim ratio: {max_victim_ratio * 100:.0f}%")
        print()
    
    # Ensure data is sorted by time
    trades_df = trades_df.sort_values('ms_time').reset_index(drop=True)
    
    fat_sandwiches = []
    detection_stats = {window: 0 for window in window_seconds}
    detection_stats['total_windows_checked'] = 0
    detection_stats['passed_aba_pattern'] = 0
    detection_stats['passed_victim_ratio'] = 0
    detection_stats['passed_token_pair'] = 0
    detection_stats['high_confidence'] = 0
    detection_stats['medium_confidence'] = 0
    
    # Group by PropAMM (sandwiches happen within same pool)
    amm_groups = trades_df.groupby('amm_trade') if 'amm_trade' in trades_df.columns else [('All', trades_df)]
    
    for amm_name, amm_trades in amm_groups:
        if verbose and len(amm_groups) > 1:
            print(f"Processing {amm_name}: {len(amm_trades):,} trades...")
        
        amm_trades = amm_trades.sort_values('ms_time').reset_index(drop=True)
        
        # Iterate through each time window size
        for window_sec in window_seconds:
            window_ms = window_sec * 1000
            
            # Sliding window detection
            i = 0
            while i < len(amm_trades):
                start_time = amm_trades.loc[i, 'ms_time']
                end_time = start_time + window_ms
                
                # Get all trades in this window
                window_mask = (amm_trades['ms_time'] >= start_time) & (amm_trades['ms_time'] <= end_time)
                window_trades = amm_trades[window_mask]
                
                detection_stats['total_windows_checked'] += 1
                
                # Check minimum trade count
                if len(window_trades) < min_trades:
                    i += 1
                    continue
                
                # Extract signers
                signers = window_trades['signer'].tolist()
                first_signer = signers[0]
                last_signer = signers[-1]
                
                # ============================================================
                # VALIDATION 1: A-B-A Pattern Check
                # ============================================================
                if first_signer != last_signer:
                    i += 1
                    continue
                
                detection_stats['passed_aba_pattern'] += 1
                attacker = first_signer
                
                # Extract middle signers (potential victims)
                middle_signers = signers[1:-1]
                unique_middle = set(middle_signers)
                
                # Must have at least 1 victim
                if len(unique_middle) == 0:
                    i += 1
                    continue
                
                # Victim cannot be the attacker (avoid wash trading)
                if attacker in unique_middle:
                    i += 1
                    continue
                
                # Count attacker's trades in window
                attacker_count = signers.count(attacker)
                if attacker_count < min_attacker_trades:
                    i += 1
                    continue
                
                # ============================================================
                # VALIDATION 2: Victim Ratio Check (Aggregator Filter)
                # ============================================================
                victim_ratio = len(unique_middle) / len(window_trades)
                if victim_ratio > max_victim_ratio:
                    # Likely aggregator routing, not MEV
                    i += 1
                    continue
                
                detection_stats['passed_victim_ratio'] += 1
                
                # ============================================================
                # VALIDATION 3: Token Pair Consistency (If Available)
                # ============================================================
                token_pair_valid = True
                if 'from_token' in window_trades.columns and 'to_token' in window_trades.columns:
                    attacker_trades = window_trades[window_trades['signer'] == attacker]
                    
                    if len(attacker_trades) >= 2:
                        # Check first and last attacker trades
                        first_trade = attacker_trades.iloc[0]
                        last_trade = attacker_trades.iloc[-1]
                        
                        first_pair = (first_trade['from_token'], first_trade['to_token'])
                        last_pair = (last_trade['from_token'], last_trade['to_token'])
                        
                        # Sandwich should have reversed token pair: (A,B) → (B,A)
                        if first_pair[0] != last_pair[1] or first_pair[1] != last_pair[0]:
                            token_pair_valid = False
                
                if not token_pair_valid:
                    i += 1
                    continue
                
                detection_stats['passed_token_pair'] += 1
                
                # ============================================================
                # CONFIDENCE SCORING
                # ============================================================
                confidence_score = 0
                confidence_reasons = []
                
                # Factor 1: Low victim ratio (more concentrated attack)
                if victim_ratio < 0.3:
                    confidence_score += 3
                    confidence_reasons.append('low_victim_ratio')
                elif victim_ratio < 0.5:
                    confidence_score += 2
                
                # Factor 2: Multiple attacker trades
                if attacker_count >= 3:
                    confidence_score += 2
                    confidence_reasons.append('multiple_attacker_trades')
                
                # Factor 3: Token pair reversal validated
                if token_pair_valid and 'from_token' in window_trades.columns:
                    confidence_score += 2
                    confidence_reasons.append('token_pair_reversal')
                
                # Factor 4: Short time window (more aggressive)
                if window_sec <= 2:
                    confidence_score += 1
                    confidence_reasons.append('short_window')
                
                # Factor 5: Multiple victims
                if len(unique_middle) >= 3:
                    confidence_score += 1
                    confidence_reasons.append('multiple_victims')
                
                # Determine final confidence
                if confidence_score >= 6:
                    confidence = 'high'
                    detection_stats['high_confidence'] += 1
                elif confidence_score >= 4:
                    confidence = 'medium'
                    detection_stats['medium_confidence'] += 1
                else:
                    confidence = 'low'
                
                # ============================================================
                # RECORD DETECTION
                # ============================================================
                detection_stats[window_sec] += 1
                
                fat_sandwiches.append({
                    'amm_trade': amm_name,
                    'attacker_signer': attacker,
                    'victim_count': len(unique_middle),
                    'victim_signers': list(unique_middle),
                    'total_trades': len(window_trades),
                    'attacker_trades': attacker_count,
                    'victim_ratio': victim_ratio,
                    'window_seconds': window_sec,
                    'window_ms': window_ms,
                    'start_slot': window_trades.iloc[0]['slot'] if 'slot' in window_trades.columns else None,
                    'end_slot': window_trades.iloc[-1]['slot'] if 'slot' in window_trades.columns else None,
                    'slot_span': window_trades.iloc[-1]['slot'] - window_trades.iloc[0]['slot'] if 'slot' in window_trades.columns else None,
                    'start_time_ms': start_time,
                    'end_time_ms': min(end_time, window_trades.iloc[-1]['ms_time']),
                    'actual_time_span_ms': window_trades.iloc[-1]['ms_time'] - window_trades.iloc[0]['ms_time'],
                    'validator': window_trades.iloc[0]['validator'] if 'validator' in window_trades.columns else None,
                    'confidence': confidence,
                    'confidence_score': confidence_score,
                    'confidence_reasons': ','.join(confidence_reasons),
                    'token_pair_validated': token_pair_valid and 'from_token' in window_trades.columns
                })
                
                # Move to next potential window
                # Skip ahead to avoid counting the same pattern multiple times
                i += max(1, attacker_count // 2)
    
    # Convert to DataFrame
    results_df = pd.DataFrame(fat_sandwiches)
    
    if verbose:
        print()
        print("=" * 80)
        print("DETECTION RESULTS")
        print("=" * 80)
        print(f"Total fat sandwiches detected: {len(results_df):,}")
        print()
        print("By Time Window:")
        for window in window_seconds:
            count = detection_stats[window]
            pct = (count / len(results_df) * 100) if len(results_df) > 0 else 0
            print(f"  {window}s window: {count:>6,} ({pct:>5.1f}%)")
        print()
        print("By Confidence:")
        print(f"  High:   {detection_stats['high_confidence']:>6,} ({detection_stats['high_confidence']/len(results_df)*100:.1f}%)" if len(results_df) > 0 else "  High: 0")
        print(f"  Medium: {detection_stats['medium_confidence']:>6,} ({detection_stats['medium_confidence']/len(results_df)*100:.1f}%)" if len(results_df) > 0 else "  Medium: 0")
        print(f"  Low:    {len(results_df) - detection_stats['high_confidence'] - detection_stats['medium_confidence']:>6,}")
        print()
        print("Validation Pass Rates:")
        print(f"  Windows checked: {detection_stats['total_windows_checked']:,}")
        print(f"  Passed A-B-A pattern: {detection_stats['passed_aba_pattern']:,} ({detection_stats['passed_aba_pattern']/detection_stats['total_windows_checked']*100:.2f}%)" if detection_stats['total_windows_checked'] > 0 else "  Passed A-B-A: 0")
        print(f"  Passed victim ratio: {detection_stats['passed_victim_ratio']:,}")
        print(f"  Passed token pair: {detection_stats['passed_token_pair']:,}")
        print()
    
    return results_df, detection_stats


def analyze_fat_sandwich_results(results_df, verbose=True):
    """
    Analyze detected fat sandwich patterns.
    
    Parameters:
    -----------
    results_df : DataFrame
        Results from detect_fat_sandwich_time_window()
    verbose : bool
        Print analysis
    
    Returns:
    --------
    analysis : dict
        Statistical analysis of results
    """
    
    if len(results_df) == 0:
        if verbose:
            print("No fat sandwiches detected.")
        return {}
    
    analysis = {}
    
    # Time span statistics
    analysis['avg_time_span_ms'] = results_df['actual_time_span_ms'].mean()
    analysis['median_time_span_ms'] = results_df['actual_time_span_ms'].median()
    analysis['max_time_span_ms'] = results_df['actual_time_span_ms'].max()
    analysis['min_time_span_ms'] = results_df['actual_time_span_ms'].min()
    
    # Victim statistics
    analysis['avg_victims'] = results_df['victim_count'].mean()
    analysis['max_victims'] = results_df['victim_count'].max()
    analysis['total_unique_victims'] = len(set([v for victims in results_df['victim_signers'] for v in victims]))
    
    # Attacker statistics
    analysis['unique_attackers'] = results_df['attacker_signer'].nunique()
    analysis['most_active_attackers'] = results_df['attacker_signer'].value_counts().head(10).to_dict()
    
    # Slot statistics
    if 'slot_span' in results_df.columns:
        analysis['avg_slot_span'] = results_df['slot_span'].mean()
        analysis['max_slot_span'] = results_df['slot_span'].max()
        analysis['single_slot_attacks'] = (results_df['slot_span'] == 0).sum()
        analysis['multi_slot_attacks'] = (results_df['slot_span'] > 0).sum()
    
    # Validator statistics
    if 'validator' in results_df.columns:
        analysis['unique_validators'] = results_df['validator'].nunique()
        analysis['top_validators'] = results_df['validator'].value_counts().head(10).to_dict()
    
    # AMM statistics
    if 'amm_trade' in results_df.columns:
        analysis['amms_affected'] = results_df['amm_trade'].nunique()
        analysis['top_amms'] = results_df['amm_trade'].value_counts().head(10).to_dict()
    
    if verbose:
        print("=" * 80)
        print("STATISTICAL ANALYSIS")
        print("=" * 80)
        print()
        print("Time Span Statistics:")
        print(f"  Average: {analysis['avg_time_span_ms']:.0f}ms ({analysis['avg_time_span_ms']/1000:.2f}s)")
        print(f"  Median:  {analysis['median_time_span_ms']:.0f}ms ({analysis['median_time_span_ms']/1000:.2f}s)")
        print(f"  Maximum: {analysis['max_time_span_ms']:.0f}ms ({analysis['max_time_span_ms']/1000:.2f}s)")
        print(f"  Minimum: {analysis['min_time_span_ms']:.0f}ms ({analysis['min_time_span_ms']/1000:.2f}s)")
        print()
        
        print("Victim Statistics:")
        print(f"  Average victims per attack: {analysis['avg_victims']:.1f}")
        print(f"  Maximum victims in single attack: {analysis['max_victims']}")
        print(f"  Total unique victims: {analysis['total_unique_victims']:,}")
        print()
        
        print("Attacker Statistics:")
        print(f"  Unique attackers: {analysis['unique_attackers']:,}")
        print(f"  Top 5 most active attackers:")
        for i, (attacker, count) in enumerate(list(analysis['most_active_attackers'].items())[:5], 1):
            print(f"    {i}. {attacker[:44]:44s}: {count:>4,} attacks")
        print()
        
        if 'slot_span' in results_df.columns:
            print("Slot Statistics:")
            print(f"  Average slot span: {analysis['avg_slot_span']:.2f} slots")
            print(f"  Maximum slot span: {analysis['max_slot_span']} slots")
            print(f"  Single-slot attacks: {analysis['single_slot_attacks']:,} ({analysis['single_slot_attacks']/len(results_df)*100:.1f}%)")
            print(f"  Multi-slot attacks: {analysis['multi_slot_attacks']:,} ({analysis['multi_slot_attacks']/len(results_df)*100:.1f}%)")
            print()
        
        if 'validator' in results_df.columns:
            print("Validator Statistics:")
            print(f"  Validators affected: {analysis['unique_validators']:,}")
            print(f"  Top 5 validators by attack count:")
            for i, (validator, count) in enumerate(list(analysis['top_validators'].items())[:5], 1):
                print(f"    {i}. {validator[:44]:44s}: {count:>4,} attacks")
            print()
        
        if 'amm_trade' in results_df.columns:
            print("PropAMM Statistics:")
            print(f"  PropAMMs affected: {analysis['amms_affected']}")
            print(f"  Top 5 PropAMMs by attack count:")
            for i, (amm, count) in enumerate(list(analysis['top_amms'].items())[:5], 1):
                print(f"    {i}. {amm:20s}: {count:>4,} attacks")
            print()
    
    return analysis


def compare_detection_methods(old_results_count, new_results_df, verbose=True):
    """
    Compare old and new detection methods.
    
    Parameters:
    -----------
    old_results_count : int
        Number of detections from old method
    new_results_df : DataFrame
        Results from new method
    verbose : bool
        Print comparison
    
    Returns:
    --------
    comparison : dict
        Comparison statistics
    """
    
    new_count = len(new_results_df)
    reduction = old_results_count - new_count
    reduction_pct = (reduction / old_results_count * 100) if old_results_count > 0 else 0
    
    # Calculate average time span for new results
    avg_time_new = new_results_df['actual_time_span_ms'].mean() / 1000 if len(new_results_df) > 0 else 0
    max_time_new = new_results_df['actual_time_span_ms'].max() / 1000 if len(new_results_df) > 0 else 0
    
    comparison = {
        'old_method_count': old_results_count,
        'new_method_count': new_count,
        'reduction': reduction,
        'reduction_percentage': reduction_pct,
        'avg_time_span_seconds': avg_time_new,
        'max_time_span_seconds': max_time_new,
        'quality_improvement': 'high' if reduction_pct > 50 else 'medium' if reduction_pct > 30 else 'low'
    }
    
    if verbose:
        print("=" * 80)
        print("METHOD COMPARISON: Old vs New")
        print("=" * 80)
        print()
        print(f"Old Method (No Time Limit):")
        print(f"  Detections: {old_results_count:,}")
        print(f"  Issues: Detected patterns spanning hours")
        print(f"  Example: 5.5 hour 'sandwich' with 102 victims")
        print()
        print(f"New Method (Rolling Time Windows):")
        print(f"  Detections: {new_count:,}")
        print(f"  Reduction: {reduction:,} ({reduction_pct:.1f}%)")
        print(f"  Average time span: {avg_time_new:.2f} seconds")
        print(f"  Maximum time span: {max_time_new:.2f} seconds")
        print()
        print(f"Quality Assessment: {comparison['quality_improvement'].upper()}")
        if reduction_pct > 70:
            print("  ✅ Excellent - Removed majority of false positives")
        elif reduction_pct > 50:
            print("  ✅ Good - Significant false positive reduction")
        elif reduction_pct > 30:
            print("  ⚠️  Moderate - Some improvement")
        else:
            print("  ❌ Low - May need parameter adjustment")
        print()
    
    return comparison


if __name__ == "__main__":
    print("Improved Fat Sandwich Detection Module")
    print("This module should be imported and used in notebooks/scripts")
    print()
    print("Example usage:")
    print("""
    from improved_fat_sandwich_detection import detect_fat_sandwich_time_window
    
    # Load your data
    df_trades = pd.read_parquet('pamm_clean_final.parquet')
    df_trades = df_trades[df_trades['kind'] == 'TRADE']
    
    # Run detection
    results, stats = detect_fat_sandwich_time_window(
        df_trades,
        window_seconds=[1, 2, 5, 10],
        min_trades=5,
        max_victim_ratio=0.8
    )
    
    # Analyze results
    analysis = analyze_fat_sandwich_results(results)
    
    # Compare with old method
    comparison = compare_detection_methods(367162, results)
    """)
