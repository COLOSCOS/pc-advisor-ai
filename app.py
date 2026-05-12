from flask import Flask, request, jsonify 
from flask_cors import CORS
import joblib
import random
import os

app = Flask(__name__)
CORS(app)

model = joblib.load("pc_model.pkl")
vectorizer = joblib.load("pc_vectorizer.pkl")

responses = {
    "greeting": ["Hello! 👋 I'm your PC Advisor. Need help with a build?", "Hey! Ready to build your PC?", "Hi there! What PC help do you need?"],
    "goodbye": ["See you later! Happy gaming! 🎮", "Bye! Come back for more PC tips!", "Goodbye! Enjoy your PC build!"],
    "thanks": ["You're welcome! 😎", "Anytime bro! Happy to help!", "No problem! Let me know if you need more help!"],
    "budget": ["For a budget PC: Ryzen 5 5600G, 16GB RAM, 500GB SSD - around ₱25,000. No dedicated GPU needed for starters!"],
    "budget_15k": ["₱15k build: Ryzen 3 3200G, 8GB RAM, 240GB SSD. Good for Valorant and Dota 2 at 60 FPS low settings."],
    "budget_20k": ["₱20k build: Ryzen 5 3400G, 16GB RAM, 480GB SSD. Good for Valorant, Dota 2 at 60-80 FPS medium settings."],
    "budget_25k": ["₱25k build: Ryzen 5 3600, GTX 1050 Ti, 16GB RAM, 500GB SSD. Great entry-level 1080p gaming."],
    "budget_30k": ["₱30k build: Ryzen 5 5600, RX 580, 16GB RAM, 500GB NVMe. Good for 1080p high settings 100+ FPS."],
    "budget_40k": ["₱40k build: Ryzen 5 5600, RX 6600, 16GB RAM, 1TB NVMe. Perfect for 1080p ultra settings 100+ FPS."],
    "valorant": ["Valorant: Ryzen 5 5600 + GTX 1650 gives 200-300 FPS at low settings. Budget: Ryzen 3 3200G gives 60-80 FPS."],
    "dota": ["Dota 2: Ryzen 5 3600 + GTX 1050 Ti gives 100+ FPS at high settings. Integrated: Ryzen 5 5600G gives 60-80 FPS."],
    "cs2": ["CS2: Ryzen 5 5600 + GTX 1650 gives 200+ FPS. Budget: Ryzen 3 3200G gives 60-80 FPS at low settings."],
    "gta": ["GTA V: GTX 1050 Ti gives 50-60 FPS at medium-high settings. For high settings, get GTX 1660 or better."],
    "minecraft": ["Minecraft: Ryzen 3 3200G gives 60-100 FPS. For shaders, get RTX 3050 or better."],
    "fortnite": ["Fortnite: GTX 1050 Ti gives 60-80 FPS. Performance mode with Ryzen 5 5600G gives 100+ FPS."],
    "gpu": ["Best GPU for 1080p: RX 6600 (₱13k-₱16k) or RTX 3060 (₱15k-₱18k). Best budget: GTX 1650 (₱7k-₱9k)."],
    "gpu_budget": ["Budget GPUs: GTX 1050 Ti (₱5k-₱7k), GTX 1650 (₱7k-₱9k), RX 580 (₱6k-₱8k)."],
    "gpu_mid": ["Mid-range GPUs: RTX 3060 (₱15k-₱18k), RX 6600 (₱13k-₱16k). Best value is RX 6600."],
    "gpu_high": ["High-end GPUs: RTX 4070 (₱35k-₱40k), RX 7800 XT (₱32k-₱38k). Perfect for 1440p ultra gaming."],
    "cpu": ["Best value CPU: Ryzen 5 5600 (₱7.5k-₱9k) or i5-12400F (₱8k-₱10k). Best budget: Ryzen 3 3200G."],
    "cpu_budget": ["Budget CPUs: Ryzen 3 3200G (₱4k-₱5.5k), Ryzen 5 3400G (₱6k-₱7.5k) for integrated graphics."],
    "cpu_mid": ["Mid-range CPUs: Ryzen 5 5600 (₱7.5k-₱9k), i5-12400F (₱8k-₱10k). Best for gaming value."],
    "ram": ["16GB RAM is the sweet spot for gaming (₱3k-₱4.5k). 32GB for streaming (₱5.5k-₱8k). 8GB minimum (₱1.5k-₱2.5k)."],
    "ram_8gb": ["8GB RAM is minimum for casual gaming. Works for Valorant, Dota 2, CS2. Costs ₱1,500-₱2,500."],
    "ram_16gb": ["16GB RAM is the sweet spot for gaming. Costs ₱3,000-₱4,500. Recommended for all mid-range builds."],
    "ram_32gb": ["32GB RAM is for streaming and video editing. Costs ₱5,500-₱8,000. Overkill for pure gaming."],
    "ssd": ["SSD is 5x faster than HDD! Get at least 500GB SSD for Windows and games. NVMe is even faster!"],
    "hdd": ["HDD is slow because it uses mechanical moving parts. HDD maxes at 80-160MB/s while SSD does 500+ MB/s."],
    "monitor": ["For 1080p gaming, 60Hz is fine for casual, 144Hz for competitive games. 144Hz monitors cost ₱8k-₱12k."],
    "monitor_144hz": ["144Hz monitors: ₱8,000-₱12,000. Brands: AOC, ViewSonic, ASUS TUF. Perfect for Valorant and CS2."],
    "monitor_240hz": ["240Hz monitors: ₱15,000-₱25,000. For serious competitive players. Only worth it if your PC can push 240+ FPS."],
    "motherboard": ["B450/B550 for AMD Ryzen, B660/B760 for Intel. Costs ₱3.5k-₱9k depending on features."],
    "psu": ["Budget builds: 500W-550W (₱2k-₱3.5k). Mid-range: 650W-750W (₱3.5k-₱5.5k). High-end: 750W-850W (₱5k-₱7k)."],
    "lag": ["Fix low FPS: Update GPU drivers, close background apps, check temps, install games on SSD not HDD."],
    "crash": ["Fix crashes: Update drivers, verify game files on Steam, check Windows updates, test RAM if persists."],
    "overheat": ["Fix overheating: Clean fans, reapply thermal paste, ensure good airflow, check fan curves in BIOS."],
    "bottleneck": ["Good pairings to avoid bottleneck: Ryzen 5 5600 + RTX 3060, i5-12400F + RX 6600. 10-15% bottleneck is fine."],
    "where_to_buy": ["Gilmore Ave in QC is the go-to place. Online: Shopee, Lazada (EasyPC, PCWorx). Physical: DataBlitz, Octagon."],
    "joke": ["Why did the PC go to therapy? Too many crashes! 😂", "What's a computer's favorite beat? An i-9! 🥁", "Why do gamers hate nature? Too much lag! 🌿"],
}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower().strip()
        
        if not user_message:
            return jsonify({'response': "Please ask me something!"})
        
        user_vectorized = vectorizer.transform([user_message])
        predicted_intent = model.predict(user_vectorized)[0]
        confidence = max(model.predict_proba(user_vectorized)[0])
        
        print(f"Message: {user_message}")
        print(f"Intent: {predicted_intent}, Confidence: {confidence:.2%}")
        
        if confidence < 0.10:
            reply = "Hmm, I'm not 100% sure about that. Try asking about PC builds, GPUs, CPUs, or specific games like Valorant or Dota!"
        else:
            reply = random.choice(responses.get(predicted_intent, ["I'm still learning about that! Try asking something about PC builds."]))
        
        return jsonify({'response': reply})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': "Having trouble processing that. Please try again!"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
