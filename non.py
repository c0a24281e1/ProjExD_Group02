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
        self.xp = 0
        self.level = 1
        self.nextlevel = self.level * 100

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
    
    def check_level(self, amount):
        """
        レベルが上がるかどうか判定する
        :param amount: 入手した経験値
        """
        self.xp += amount
        messages = [f"{self.name}は経験値{amount}を獲得した！"]
        while self.xp >= self.nextlevel:
            if self.level >= 99:
                self.xp = self.nextlevel - 1
                break
            self.xp -= self.nextlevel
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            self.attack_power += 3
            self.defense_power += 2

            self.nextlevel = self.level * 100
            messages.append(f"{self.name}はレベル{self.level}に上がった！")
        return messages 


def draw_xp_bar(surface, unit, x, y, bar_width=200, bar_height=10):
    if unit.nextlevel == 0 or unit.level >= 99:
        ratio = 1.0
    else:
        ratio = unit.xp / unit.nextlevel
    
    xp_color = (150, 150, 255)

    background_rect = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(surface, WHITE, background_rect, 1)

    current_width = int(bar_width * ratio)
    xp_rect = pygame.Rect(x, y, current_width, bar_height)
    pygame.draw.rect(surface, xp_color, xp_rect)


def draw_health_bar(surface, unit, x, y, bar_width=200, bar_height=20):
    """
    指定されたUnitのHPバーを描画する関数
    
    surface: 描画先のPygame Surface (screen)
    unit: HPを持つUnitオブジェクト
    x: バーの左上X座標
    y: バーの左上Y座標
    bar_width: バーの全体の幅
    bar_height: バーの高さ
    """
    
    # HPの割合を計算
    ratio = unit.hp / unit.max_hp
    
    # 描画色を決定（勇者は緑、魔王は赤など）
    if unit.name == "勇者":
        bar_color = (0, 255, 0) 
    else:
        bar_color = RED         

    # 1. バーの背景（全体）を描画
    background_rect = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(surface, WHITE, background_rect, 1) # 白い枠線
    
    # 2. 現在のHPに応じたバー（中身）を描画
    current_width = int(bar_width * ratio)  
    hp_rect = pygame.Rect(x, y, current_width, bar_height)
    pygame.draw.rect(surface, bar_color, hp_rect)

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
        if event.type == pygame.QUIT:
            running = False
            # ウィンドウの閉じるボタンが押されたらループを抜ける
            break
        
        # スペースキーが押されたらターンを進める
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_over:
                if turn == "PLAYER":
                    # 勇者の攻撃処理
                    msg = hero.attack(demon)
                    battle_logs.append(msg) # ログに追加
                    
                    if not demon.is_alive():
                        battle_logs.append("魔王を倒した！")
                        xp_messages = hero.check_level(200)
                        battle_logs.extend(xp_messages)
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
    draw_health_bar(screen, hero, 50, 80)
    draw_health_bar(screen, demon, 400, 80)
    draw_xp_bar(screen, hero, 50, 100)

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