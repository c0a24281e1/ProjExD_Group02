import pygame
import random
import sys

# --- 1. 設定とクラス定義 ---

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 100, 100)

class Unit:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack
        self.defense_power = defense

    def is_alive(self):
        """生きているかどうかの判定"""
        return self.hp > 0

    def attack(self, target):
        """targetに対して攻撃し、ダメージ計算結果とメッセージを返す"""
        
        # ダメージ計算式： (自分の攻撃力 - 相手の防御力) + 乱数(-3〜+3)
        base_damage = self.attack_power - target.defense_power
        variance = random.randint(-3, 3) 
        damage = base_damage + variance

        # ダメージは最低でも1入るようにする（0やマイナスを防ぐ）
        if damage < 1:
            damage = 1

        # 相手のHPを減らす
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0

        # ログ用のメッセージを作成して返す
        return f"{self.name}の攻撃！ {target.name}に {damage} のダメージ！"

# --- 2. Pygame初期化 ---
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("テキストバトル RPG")

# 日本語フォントの設定（環境に合わせてフォントを探します）
font_name = pygame.font.match_font('meiryo', 'yu gothic', 'hiragino maru gothic pro')
font = pygame.font.Font(font_name, 24)

# --- 3. ゲームデータの準備 ---
hero = Unit(name="勇者", hp=100, attack=30, defense=10)
demon = Unit(name="魔王", hp=250, attack=25, defense=5)

# 戦闘ログ（画面に表示するテキストのリスト）
battle_logs = ["スペースキーを押してバトル開始！"]

turn = "PLAYER" # どちらのターンか
game_over = False

# --- 4. メインループ ---
running = True
while running:
    screen.fill(BLACK) # 画面をリセット

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False
        
        # スペースキーが押されたらターンを進める
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_over:
                if turn == "PLAYER":
                    # 勇者の攻撃処理
                    msg = hero.attack(demon)
                    battle_logs.append(msg) # ログに追加
                    
                    if not demon.is_alive():
                        battle_logs.append("魔王を倒した！")
                        game_over = True
                    else:
                        turn = "ENEMY" # 相手のターンへ
                
                elif turn == "ENEMY":
                    # 魔王の攻撃処理
                    msg = demon.attack(hero)
                    battle_logs.append(msg)
                    
                    if not hero.is_alive():
                        battle_logs.append("勇者は力尽きた...")
                        game_over = True
                    else:
                        turn = "PLAYER" # プレイヤーのターンへ
            else:
                # ゲームオーバー後
                battle_logs.append("ゲーム終了。閉じるボタンで終了してください。")

    # --- 描画処理 ---
    
    # 1. ステータス表示（画面上部）
    hero_text = font.render(f"{hero.name} HP: {hero.hp}/{hero.max_hp}", True, WHITE)
    demon_text = font.render(f"{demon.name} HP: {demon.hp}/{demon.max_hp}", True, RED)
    screen.blit(hero_text, (50, 50))
    screen.blit(demon_text, (400, 50))

    # 2. ログの表示（最新の5行だけ表示する）
    # リストの後ろから5つを取得して表示
    recent_logs = battle_logs[-5:] 
    
    y = 150 # テキストを表示し始めるY座標
    for log in recent_logs:
        text_surface = font.render(log, True, WHITE)
        screen.blit(text_surface, (50, y))
        y += 40 # 行間をあける

    # 3. 操作ガイド
    if not game_over:
        guide_text = font.render("[SPACE]でターンを進める", True, (100, 255, 100))
        screen.blit(guide_text, (200, 400))

    pygame.display.flip()

pygame.quit()
sys.exit()