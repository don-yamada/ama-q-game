#!/usr/bin/env python3
# シンプルなテキストベースのアドベンチャーゲーム

import time
import random

class Game:
    def __init__(self):
        self.player_name = ""
        self.player_health = 100
        self.player_score = 0
        self.game_running = True
        
    def start(self):
        """ゲームを開始する"""
        self.show_intro()
        self.player_name = input("あなたの名前を入力してください: ")
        print(f"\nようこそ {self.player_name}さん！冒険を始めましょう！\n")
        time.sleep(1)
        
        while self.game_running:
            self.show_status()
            choice = self.show_options()
            self.process_choice(choice)
            
            if self.player_health <= 0:
                print("\nゲームオーバー！あなたは力尽きてしまいました...")
                self.game_running = False
            elif self.player_score >= 100:
                print("\nおめでとうございます！あなたは冒険に勝利しました！")
                self.game_running = False
        
        print(f"\n最終スコア: {self.player_score}")
        print("また遊んでくださいね！")
    
    def show_intro(self):
        """ゲームの導入部分を表示する"""
        print("=" * 60)
        print("          不思議な森の冒険          ")
        print("=" * 60)
        print("あなたは不思議な森に迷い込みました。")
        print("森から脱出するためには、様々な試練を乗り越える必要があります。")
        print("健康に気をつけながら、100ポイントを集めて森から脱出しましょう！")
        print("=" * 60)
        time.sleep(2)
    
    def show_status(self):
        """プレイヤーのステータスを表示する"""
        print("\n" + "-" * 30)
        print(f"名前: {self.player_name}")
        print(f"体力: {self.player_health}")
        print(f"スコア: {self.player_score}")
        print("-" * 30 + "\n")
    
    def show_options(self):
        """プレイヤーの選択肢を表示する"""
        print("何をしますか？")
        print("1: 森を探索する")
        print("2: 休憩する")
        print("3: 宝箱を開ける（リスクあり）")
        print("4: ゲームを終了する")
        
        while True:
            try:
                choice = int(input("選択肢の番号を入力してください: "))
                if 1 <= choice <= 4:
                    return choice
                else:
                    print("1から4の数字を入力してください。")
            except ValueError:
                print("数字を入力してください。")
    
    def process_choice(self, choice):
        """プレイヤーの選択を処理する"""
        if choice == 1:
            self.explore()
        elif choice == 2:
            self.rest()
        elif choice == 3:
            self.open_chest()
        elif choice == 4:
            print("\nゲームを終了します...")
            self.game_running = False
    
    def explore(self):
        """森を探索する"""
        print("\n森を探索しています...")
        time.sleep(1)
        
        events = [
            "小さな妖精を見つけました！スコア+10",
            "美しい花を見つけました！スコア+5",
            "野生の動物に遭遇しました！体力-10",
            "毒のある植物に触れてしまいました！体力-15",
            "何も見つかりませんでした。",
            "小さな泉を見つけました！体力+10"
        ]
        
        event = random.choice(events)
        print(event)
        
        if "スコア+10" in event:
            self.player_score += 10
        elif "スコア+5" in event:
            self.player_score += 5
        elif "体力-10" in event:
            self.player_health -= 10
        elif "体力-15" in event:
            self.player_health -= 15
        elif "体力+10" in event:
            self.player_health += 10
            if self.player_health > 100:
                self.player_health = 100
    
    def rest(self):
        """休憩して体力を回復する"""
        print("\n休憩しています...")
        time.sleep(2)
        
        recovery = random.randint(10, 20)
        self.player_health += recovery
        if self.player_health > 100:
            self.player_health = 100
        
        print(f"体力が{recovery}ポイント回復しました！")
    
    def open_chest(self):
        """宝箱を開ける（リスクとリターン）"""
        print("\n宝箱を開けています...")
        time.sleep(2)
        
        result = random.randint(1, 10)
        
        if result <= 3:  # 30%の確率で罠
            damage = random.randint(10, 25)
            self.player_health -= damage
            print(f"罠でした！体力が{damage}ポイント減少しました。")
        elif result <= 8:  # 50%の確率で宝物
            points = random.randint(10, 20)
            self.player_score += points
            print(f"宝物を見つけました！スコアが{points}ポイント増加しました。")
        else:  # 20%の確率で大当たり
            points = random.randint(20, 30)
            self.player_score += points
            print(f"素晴らしい宝物を見つけました！スコアが{points}ポイント増加しました。")

if __name__ == "__main__":
    game = Game()
    game.start()
