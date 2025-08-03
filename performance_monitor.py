#!/usr/bin/env python3
"""
Performance monitoring script for FluentPass
Tracks key performance metrics and provides optimization recommendations
"""

import time
import psutil
import sqlite3
import os
import requests
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.db_path = os.path.join(".", 'fluentpass.db')
        self.base_url = "http://localhost:5000"
        
    def check_database_performance(self):
        """Check database performance metrics"""
        try:
            start_time = time.time()
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Test query performance
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            # Check database size
            db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            query_time = (time.time() - start_time) * 1000  # Convert to ms
            
            conn.close()
            
            return {
                "query_time_ms": round(query_time, 2),
                "user_count": user_count,
                "db_size_mb": round(db_size / (1024 * 1024), 2),
                "status": "healthy" if query_time < 100 else "slow"
            }
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def check_server_performance(self):
        """Check server performance metrics"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            return {
                "memory_used_percent": memory.percent,
                "memory_available_mb": round(memory.available / (1024 * 1024), 2),
                "cpu_percent": cpu_percent,
                "disk_used_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024 * 1024 * 1024), 2)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def check_response_times(self):
        """Check HTTP response times"""
        endpoints = [
            "/",
            "/api/health",
            "/assets/index-ChLEs4-J.js",
            "/assets/index-IlUsjxHz.css"
        ]
        
        results = {}
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                response_time = (time.time() - start_time) * 1000
                
                results[endpoint] = {
                    "response_time_ms": round(response_time, 2),
                    "status_code": response.status_code,
                    "content_length": len(response.content),
                    "status": "fast" if response_time < 200 else "slow" if response_time < 1000 else "very_slow"
                }
            except Exception as e:
                results[endpoint] = {"error": str(e), "status": "error"}
        
        return results
    
    def analyze_bundle_sizes(self):
        """Analyze frontend bundle sizes"""
        assets_dir = "assets"
        results = {}
        
        if os.path.exists(assets_dir):
            for filename in os.listdir(assets_dir):
                file_path = os.path.join(assets_dir, filename)
                if os.path.isfile(file_path):
                    size_bytes = os.path.getsize(file_path)
                    size_kb = round(size_bytes / 1024, 2)
                    
                    # Determine if size is optimal
                    status = "optimal"
                    if filename.endswith('.js') and size_kb > 200:
                        status = "large"
                    elif filename.endswith('.css') and size_kb > 100:
                        status = "large"
                    
                    results[filename] = {
                        "size_kb": size_kb,
                        "size_bytes": size_bytes,
                        "status": status
                    }
        
        return results
    
    def generate_recommendations(self, metrics):
        """Generate performance optimization recommendations"""
        recommendations = []
        
        # Database recommendations
        if "database" in metrics:
            db_metrics = metrics["database"]
            if db_metrics.get("query_time_ms", 0) > 50:
                recommendations.append("Consider adding database indexes for slow queries")
            if db_metrics.get("db_size_mb", 0) > 100:
                recommendations.append("Database size is large, consider archiving old data")
        
        # Server recommendations
        if "server" in metrics:
            server_metrics = metrics["server"]
            if server_metrics.get("memory_used_percent", 0) > 80:
                recommendations.append("High memory usage detected, consider scaling up")
            if server_metrics.get("cpu_percent", 0) > 80:
                recommendations.append("High CPU usage detected, consider optimizing code or scaling")
        
        # Response time recommendations
        if "response_times" in metrics:
            for endpoint, data in metrics["response_times"].items():
                if data.get("response_time_ms", 0) > 500:
                    recommendations.append(f"Slow response time for {endpoint}, consider caching")
        
        # Bundle size recommendations
        if "bundles" in metrics:
            for filename, data in metrics["bundles"].items():
                if data.get("status") == "large":
                    if filename.endswith('.js'):
                        recommendations.append(f"JavaScript bundle {filename} is large, consider code splitting")
                    elif filename.endswith('.css'):
                        recommendations.append(f"CSS bundle {filename} is large, consider purging unused styles")
        
        return recommendations
    
    def run_full_analysis(self):
        """Run complete performance analysis"""
        print("🚀 FluentPass Performance Analysis")
        print("=" * 50)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        metrics = {}
        
        # Database performance
        print("📊 Database Performance:")
        db_metrics = self.check_database_performance()
        metrics["database"] = db_metrics
        for key, value in db_metrics.items():
            print(f"  {key}: {value}")
        print()
        
        # Server performance
        print("🖥️  Server Performance:")
        server_metrics = self.check_server_performance()
        metrics["server"] = server_metrics
        for key, value in server_metrics.items():
            print(f"  {key}: {value}")
        print()
        
        # Bundle analysis
        print("📦 Bundle Analysis:")
        bundle_metrics = self.analyze_bundle_sizes()
        metrics["bundles"] = bundle_metrics
        for filename, data in bundle_metrics.items():
            print(f"  {filename}: {data['size_kb']}KB ({data['status']})")
        print()
        
        # Response times (only if server is running)
        print("⚡ Response Times:")
        try:
            response_metrics = self.check_response_times()
            metrics["response_times"] = response_metrics
            for endpoint, data in response_metrics.items():
                if "error" not in data:
                    print(f"  {endpoint}: {data['response_time_ms']}ms ({data['status']})")
                else:
                    print(f"  {endpoint}: Error - {data['error']}")
        except:
            print("  Server not running - skipping response time checks")
        print()
        
        # Recommendations
        print("💡 Optimization Recommendations:")
        recommendations = self.generate_recommendations(metrics)
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print("  ✅ No major performance issues detected!")
        
        return metrics

if __name__ == "__main__":
    monitor = PerformanceMonitor()
    monitor.run_full_analysis()