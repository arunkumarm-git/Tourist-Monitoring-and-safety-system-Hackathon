import numpy as np
from sklearn.cluster import DBSCAN
from typing import List, Dict
from collections import defaultdict

class TouristClusterer:
    def __init__(self, epsilon_meters: int = 50, min_samples: int = 8):
        self.epsilon_meters = epsilon_meters
        self.min_samples = min_samples
        self.earth_radius = 6371000
    
    def cluster_positions(self, positions: List[Dict]) -> Dict:
        if not positions:
            return {"tourists": [], "clusters": [], "stats": {"total_tourists": 0, "num_clusters": 0, "outliers": 0}}
        
        coords = np.array([[p["lat"], p["lng"]] for p in positions])
        tourist_ids = [p["id"] for p in positions]
        
        X = np.radians(coords)
        eps_rad = self.epsilon_meters / self.earth_radius
        
        dbscan = DBSCAN(eps=eps_rad, min_samples=self.min_samples, metric='haversine')
        cluster_labels = dbscan.fit_predict(X)
        
        tourist_results = []
        cluster_summary = defaultdict(lambda: {"lats": [], "lngs": [], "count": 0, "tourists": []})
        
        for tid, label, (lat, lng) in zip(tourist_ids, cluster_labels, coords):
            tourist_results.append({
                "id": tid,
                "lat": float(lat),
                "lng": float(lng),
                "cluster_id": int(label),
                "is_outlier": label == -1
            })
            
            if label != -1:
                cluster_summary[label]["lats"].append(lat)
                cluster_summary[label]["lngs"].append(lng)
                cluster_summary[label]["count"] += 1
                cluster_summary[label]["tourists"].append(tid)
        
        clusters = []
        for cluster_id, data in cluster_summary.items():
            center_lat = np.mean(data["lats"])
            center_lng = np.mean(data["lngs"])
            clusters.append({
                "cluster_id": int(cluster_id),
                "center_lat": round(float(center_lat), 6),
                "center_lng": round(float(center_lng), 6),
                "count": data["count"]
            })
        
        clusters.sort(key=lambda x: x["count"], reverse=True)
        outlier_count = sum(1 for t in tourist_results if t["is_outlier"])
        
        return {
            "tourists": tourist_results,
            "clusters": clusters,
            "stats": {
                "total_tourists": len(tourist_results),
                "num_clusters": len(clusters),
                "outliers": outlier_count
            }
        }
    
    def get_outliers(self, clustering_result: Dict) -> List[str]:
        return [t["id"] for t in clustering_result["tourists"] if t["is_outlier"]]
    
    def get_cluster_members(self, clustering_result: Dict, cluster_id: int) -> List[str]:
        return [t["id"] for t in clustering_result["tourists"] if t["cluster_id"] == cluster_id]