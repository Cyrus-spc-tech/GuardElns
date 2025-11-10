"""
Risk Profiling Engine
Assigns threat scores to devices and users based on behavior
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict


class RiskProfile:
    """Individual risk profile for a device or user"""
    
    def __init__(self, entity_id, entity_type='device'):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.risk_score = 0.0
        self.anomaly_count = 0
        self.total_events = 0
        self.first_seen = datetime.now()
        self.last_seen = datetime.now()
        self.behaviors = defaultdict(int)
        self.risk_factors = {}
        
    def update(self, event_data, is_anomaly=False):
        """Update profile with new event"""
        self.total_events += 1
        self.last_seen = datetime.now()
        
        if is_anomaly:
            self.anomaly_count += 1
        
        # Track behaviors
        if 'protocol' in event_data:
            self.behaviors[f"protocol_{event_data['protocol']}"] += 1
        if 'dst_port' in event_data:
            self.behaviors[f"port_{event_data['dst_port']}"] += 1
        
        # Calculate risk score
        self._calculate_risk_score()
    
    def _calculate_risk_score(self):
        """Calculate overall risk score (0-100)"""
        # Base score from anomaly rate
        anomaly_rate = self.anomaly_count / max(self.total_events, 1)
        base_score = anomaly_rate * 100
        
        # Adjust for unusual behaviors
        behavior_penalty = 0
        if len(self.behaviors) > 10:  # Too many different behaviors
            behavior_penalty += 10
        
        # Adjust for activity level
        activity_factor = min(self.total_events / 1000, 1.0) * 10
        
        # Calculate final score
        self.risk_score = min(base_score + behavior_penalty + activity_factor, 100)
        
        # Update risk factors
        self.risk_factors = {
            'anomaly_rate': round(anomaly_rate * 100, 2),
            'behavior_diversity': len(self.behaviors),
            'activity_level': self.total_events,
            'days_active': (self.last_seen - self.first_seen).days
        }
    
    def get_risk_level(self):
        """Get categorical risk level"""
        if self.risk_score < 30:
            return 'LOW'
        elif self.risk_score < 70:
            return 'MEDIUM'
        else:
            return 'HIGH'
    
    def to_dict(self):
        """Convert profile to dictionary"""
        return {
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'risk_score': round(self.risk_score, 2),
            'risk_level': self.get_risk_level(),
            'anomaly_count': self.anomaly_count,
            'total_events': self.total_events,
            'first_seen': self.first_seen.isoformat(),
            'last_seen': self.last_seen.isoformat(),
            'risk_factors': self.risk_factors
        }


class RiskEngine:
    """Manages risk profiles for all entities"""
    
    def __init__(self):
        self.profiles = {}
        self.history = []
        
    def get_or_create_profile(self, entity_id, entity_type='device'):
        """Get existing profile or create new one"""
        if entity_id not in self.profiles:
            self.profiles[entity_id] = RiskProfile(entity_id, entity_type)
        return self.profiles[entity_id]
    
    def update_from_traffic(self, df, predictions=None):
        """Update profiles from traffic data"""
        if df.empty:
            return
        
        for idx, row in df.iterrows():
            # Update source IP profile
            if pd.notna(row.get('src_ip')):
                profile = self.get_or_create_profile(row['src_ip'], 'device')
                is_anomaly = predictions[idx] == 1 if predictions is not None and idx < len(predictions) else False
                profile.update(row.to_dict(), is_anomaly)
            
            # Update destination IP profile
            if pd.notna(row.get('dst_ip')):
                profile = self.get_or_create_profile(row['dst_ip'], 'device')
                is_anomaly = predictions[idx] == 1 if predictions is not None and idx < len(predictions) else False
                profile.update(row.to_dict(), is_anomaly)
        
        # Record history snapshot
        self._record_history()
    
    def _record_history(self):
        """Record current state for trend analysis"""
        snapshot = {
            'timestamp': datetime.now(),
            'total_profiles': len(self.profiles),
            'high_risk_count': sum(1 for p in self.profiles.values() if p.get_risk_level() == 'HIGH'),
            'medium_risk_count': sum(1 for p in self.profiles.values() if p.get_risk_level() == 'MEDIUM'),
            'low_risk_count': sum(1 for p in self.profiles.values() if p.get_risk_level() == 'LOW'),
            'avg_risk_score': np.mean([p.risk_score for p in self.profiles.values()]) if self.profiles else 0
        }
        self.history.append(snapshot)
        
        # Keep only last 1000 snapshots
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
    
    def get_high_risk_entities(self, threshold=70):
        """Get entities with risk score above threshold"""
        high_risk = []
        for profile in self.profiles.values():
            if profile.risk_score >= threshold:
                high_risk.append(profile.to_dict())
        return sorted(high_risk, key=lambda x: x['risk_score'], reverse=True)
    
    def get_all_profiles(self):
        """Get all risk profiles"""
        return [p.to_dict() for p in self.profiles.values()]
    
    def get_profile(self, entity_id):
        """Get specific profile"""
        if entity_id in self.profiles:
            return self.profiles[entity_id].to_dict()
        return None
    
    def get_statistics(self):
        """Get overall risk statistics"""
        if not self.profiles:
            return {
                'total_entities': 0,
                'high_risk': 0,
                'medium_risk': 0,
                'low_risk': 0,
                'avg_risk_score': 0,
                'max_risk_score': 0
            }
        
        risk_scores = [p.risk_score for p in self.profiles.values()]
        
        return {
            'total_entities': len(self.profiles),
            'high_risk': sum(1 for p in self.profiles.values() if p.get_risk_level() == 'HIGH'),
            'medium_risk': sum(1 for p in self.profiles.values() if p.get_risk_level() == 'MEDIUM'),
            'low_risk': sum(1 for p in self.profiles.values() if p.get_risk_level() == 'LOW'),
            'avg_risk_score': round(np.mean(risk_scores), 2),
            'max_risk_score': round(max(risk_scores), 2),
            'min_risk_score': round(min(risk_scores), 2)
        }
    
    def get_risk_trend(self, hours=24):
        """Get risk trend over time"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_history = [h for h in self.history if h['timestamp'] > cutoff]
        return recent_history
    
    def reset_profile(self, entity_id):
        """Reset a specific profile"""
        if entity_id in self.profiles:
            del self.profiles[entity_id]
            return True
        return False
    
    def clear_all_profiles(self):
        """Clear all profiles"""
        self.profiles.clear()
        self.history.clear()
