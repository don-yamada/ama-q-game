import pygame
import random
import sys
import os
import time
import webbrowser

# ゲームの初期化
pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AWS Service Sorter - クラウドマスターへの道")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# 虹色のグラデーション用の色
RAINBOW_COLORS = [
    (255, 0, 0),  # 赤
    (255, 127, 0),  # オレンジ
    (255, 255, 0),  # 黄
    (0, 255, 0),  # 緑
    (0, 0, 255),  # 青
    (75, 0, 130),  # インディゴ
    (148, 0, 211),  # バイオレット
]

# ゲームモード
NORMAL_MODE = 0  # 接頭辞あり
HARD_MODE = 1  # 接頭辞なし

# プレイモード
TIME_ATTACK = 0  # 制限時間内モード
COMPLETE_ALL = 1  # 全サービス仕分けモード

# フォント - 日本語対応
try:
    # macOSの場合、Hiragino Sansを使用
    if sys.platform == "darwin":
        font_paths = [
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/AppleGothic.ttf",
        ]

        font_path = None
        for path in font_paths:
            if os.path.exists(path):
                font_path = path
                break

        if font_path:
            font_large = pygame.font.Font(font_path, 36)
            font_medium = pygame.font.Font(font_path, 24)
            font_small = pygame.font.Font(font_path, 18)
        else:
            # フォントが見つからない場合はデフォルトを使用
            font_large = pygame.font.Font(pygame.font.get_default_font(), 36)
            font_medium = pygame.font.Font(pygame.font.get_default_font(), 24)
            font_small = pygame.font.Font(pygame.font.get_default_font(), 18)
    else:
        # その他のOSの場合
        font_large = pygame.font.Font(pygame.font.get_default_font(), 36)
        font_medium = pygame.font.Font(pygame.font.get_default_font(), 24)
        font_small = pygame.font.Font(pygame.font.get_default_font(), 18)
except Exception as e:
    print(f"フォント読み込みエラー: {e}")
    font_large = pygame.font.Font(pygame.font.get_default_font(), 36)
    font_medium = pygame.font.Font(pygame.font.get_default_font(), 24)
    font_small = pygame.font.Font(pygame.font.get_default_font(), 18)

# AWSサービスの公式URL（サービス名をキーとする辞書）
aws_service_urls = {
    # AWSで始まるサービス
    "AWS Lambda": "https://aws.amazon.com/lambda/",
    "AWS IAM": "https://aws.amazon.com/iam/",
    "AWS CloudFormation": "https://aws.amazon.com/cloudformation/",
    "AWS CloudWatch": "https://aws.amazon.com/cloudwatch/",
    "AWS CloudTrail": "https://aws.amazon.com/cloudtrail/",
    "AWS Config": "https://aws.amazon.com/config/",
    "AWS Glue": "https://aws.amazon.com/glue/",
    "AWS Step Functions": "https://aws.amazon.com/step-functions/",
    "AWS AppSync": "https://aws.amazon.com/appsync/",
    "AWS Amplify": "https://aws.amazon.com/amplify/",
    "AWS Fargate": "https://aws.amazon.com/fargate/",
    # Amazonで始まるサービス
    "Amazon EC2": "https://aws.amazon.com/ec2/",
    "Amazon S3": "https://aws.amazon.com/s3/",
    "Amazon RDS": "https://aws.amazon.com/rds/",
    "Amazon DynamoDB": "https://aws.amazon.com/dynamodb/",
    "Amazon SQS": "https://aws.amazon.com/sqs/",
    "Amazon SNS": "https://aws.amazon.com/sns/",
    "Amazon VPC": "https://aws.amazon.com/vpc/",
    "Amazon Route 53": "https://aws.amazon.com/route53/",
    "Amazon CloudFront": "https://aws.amazon.com/cloudfront/",
    "Amazon ECS": "https://aws.amazon.com/ecs/",
    "Amazon EKS": "https://aws.amazon.com/eks/",
    "Amazon SageMaker": "https://aws.amazon.com/sagemaker/",
    "Amazon Redshift": "https://aws.amazon.com/redshift/",
    "Amazon Athena": "https://aws.amazon.com/athena/",
    "Amazon EMR": "https://aws.amazon.com/emr/",
    "Amazon Kinesis": "https://aws.amazon.com/kinesis/",
    "Amazon QuickSight": "https://aws.amazon.com/quicksight/",
    "Amazon Comprehend": "https://aws.amazon.com/comprehend/",
    "Amazon Rekognition": "https://aws.amazon.com/rekognition/",
    "Amazon Polly": "https://aws.amazon.com/polly/",
    "Amazon Lex": "https://aws.amazon.com/lex/",
    "Amazon Connect": "https://aws.amazon.com/connect/",
    "Amazon Pinpoint": "https://aws.amazon.com/pinpoint/",
    "Amazon OpenSearch Service": "https://aws.amazon.com/opensearch-service/",
    "Amazon Neptune": "https://aws.amazon.com/neptune/",
    "Amazon DocumentDB": "https://aws.amazon.com/documentdb/",
    "Amazon ElastiCache": "https://aws.amazon.com/elasticache/",
    "Amazon API Gateway": "https://aws.amazon.com/api-gateway/",
    "Amazon Elastic Beanstalk": "https://aws.amazon.com/elasticbeanstalk/",
    "Amazon GuardDuty": "https://aws.amazon.com/guardduty/",
    "Amazon Inspector": "https://aws.amazon.com/inspector/",
    "Amazon Macie": "https://aws.amazon.com/macie/",
    "Amazon Secrets Manager": "https://aws.amazon.com/secrets-manager/",
    "Amazon CodeBuild": "https://aws.amazon.com/codebuild/",
    "Amazon CodePipeline": "https://aws.amazon.com/codepipeline/",
    "Amazon CodeDeploy": "https://aws.amazon.com/codedeploy/",
    # その他のサービス
    "Savings Plans": "https://aws.amazon.com/savingsplans/",
    "EC2 Image Builder": "https://aws.amazon.com/image-builder/",
    "Elastic Load Balancing": "https://aws.amazon.com/elasticloadbalancing/",
    "FreeRTOS": "https://aws.amazon.com/freertos/",
}

# AWSサービスのリスト
aws_services = list(aws_service_urls.keys())
# ハードモード用のサービスリスト（接頭辞なし）
hard_mode_services = {
    # AWSで始まるサービス
    "left": [
        "Lambda",
        "IAM",
        "CloudFormation",
        "CloudWatch",
        "CloudTrail",
        "Config",
        "Glue",
        "Step Functions",
        "AppSync",
        "Amplify",
        "Fargate",
    ],
    # Amazonで始まるサービス
    "right": [
        "EC2",
        "S3",
        "RDS",
        "DynamoDB",
        "SQS",
        "SNS",
        "VPC",
        "Route 53",
        "CloudFront",
        "ECS",
        "EKS",
        "SageMaker",
        "Redshift",
        "Athena",
        "EMR",
        "Kinesis",
        "QuickSight",
        "Comprehend",
        "Rekognition",
        "Polly",
        "Lex",
        "Connect",
        "Pinpoint",
        "OpenSearch Service",
        "Neptune",
        "DocumentDB",
        "ElastiCache",
        "API Gateway",
        "Elastic Beanstalk",
        "GuardDuty",
        "Inspector",
        "Macie",
        "Secrets Manager",
        "CodeBuild",
        "CodePipeline",
        "CodeDeploy",
    ],
    # その他のサービス
    "bottom": [
        "Savings Plans",
        "EC2 Image Builder",
        "Elastic Load Balancing",
        "FreeRTOS",
    ],
}

# ハードモード用のサービスURLマッピング
hard_mode_service_urls = {}
for service_type in hard_mode_services:
    for service in hard_mode_services[service_type]:
        # 対応する完全なサービス名を見つける
        for full_name, url in aws_service_urls.items():
            if full_name.endswith(service):
                hard_mode_service_urls[service] = url
                break

        # 全サービス一覧画面
        # サービス一覧ページは削除しました

        pygame.display.flip()
        pygame.time.Clock().tick(60)


# ゲームの状態
class GameState:
    def __init__(self, difficulty_mode=NORMAL_MODE, play_mode=TIME_ATTACK):
        self.score = 0
        self.level = 1
        self.difficulty_mode = difficulty_mode  # 難易度モード（NORMAL/HARD）
        self.play_mode = play_mode  # プレイモード（TIME_ATTACK/COMPLETE_ALL）
        self.game_over = False
        self.current_service = None
        self.current_type = None
        self.display_timer = 0
        self.result_display = None
        self.result_timer = 0
        self.result_position = (
            WIDTH // 2,
            HEIGHT // 2 - 100,
        )  # 結果表示位置（サービス名の上）
        self.feedback_symbol = None  # ◯/×の表示
        self.symbol_timer = 0  # シンボルタイマー
        self.combo_count = 0  # コンボカウント
        self.last_answer_time = 0  # 最後に回答した時間
        self.answer_time_limit = 3.0  # コンボが途切れる時間（秒）
        self.mistakes = 0  # 間違えた回数

        # 制限時間モード用
        self.time_limit = 60  # 60秒
        self.start_time = None
        self.remaining_time = self.time_limit
        self.time_bonus_added = False  # 時間ボーナスが追加されたかのフラグ
        self.end_time = None  # 終了時間を記録

        # 全サービス仕分けモード用
        if self.play_mode == COMPLETE_ALL:
            if self.difficulty_mode == NORMAL_MODE:
                self.services_to_sort = aws_services.copy()
            else:
                # ハードモードの場合は3つのカテゴリを結合
                self.services_to_sort = (
                    hard_mode_services["left"]
                    + hard_mode_services["right"]
                    + hard_mode_services["bottom"]
                )
            random.shuffle(self.services_to_sort)
            self.total_services = len(self.services_to_sort)
            self.sorted_services = 0
            self.start_time = time.time()  # 全サービスモードでも時間を計測

        # 称号リスト
        self.titles = [
            {"min_score": 1000, "title": "AWSの王", "color": (255, 215, 0)},  # 金色
            {
                "min_score": 900,
                "title": "AWSのSAもびっくり！",
                "color": (255, 140, 0),
            },  # オレンジ
            {
                "min_score": 800,
                "title": "クラウドアーキテクト",
                "color": (30, 144, 255),
            },  # ドジャーブルー
            {
                "min_score": 700,
                "title": "AWSマスター",
                "color": (138, 43, 226),
            },  # ブルーバイオレット
            {
                "min_score": 600,
                "title": "クラウドの達人",
                "color": (0, 191, 255),
            },  # ディープスカイブルー
            {
                "min_score": 500,
                "title": "AWSエキスパート",
                "color": (50, 205, 50),
            },  # ライムグリーン
            {
                "min_score": 400,
                "title": "クラウドエンジニア",
                "color": (255, 105, 180),
            },  # ホットピンク
            {
                "min_score": 300,
                "title": "AWSプラクティショナー",
                "color": (65, 105, 225),
            },  # ロイヤルブルー
            {
                "min_score": 200,
                "title": "クラウド見習い",
                "color": (100, 149, 237),
            },  # コーンフラワーブルー
            {
                "min_score": 100,
                "title": "AWSビギナー",
                "color": (169, 169, 169),
            },  # ダークグレー
            {
                "min_score": 0,
                "title": "クラウド初心者",
                "color": (192, 192, 192),
            },  # シルバー
        ]

        # 次のサービスを表示
        self.next_service()

    def next_service(self):
        """次のサービスを選択して表示する"""
        if self.play_mode == COMPLETE_ALL and not self.services_to_sort:
            # 全サービス仕分け完了
            self.game_over = True
            return

        if self.difficulty_mode == NORMAL_MODE:
            if self.play_mode == TIME_ATTACK:
                # 制限時間モードではランダムに選択
                service = random.choice(aws_services)
            else:
                # 全サービス仕分けモードでは残りのサービスから選択
                service = self.services_to_sort.pop(0)

            # サービスの種類を判定
            if service.startswith("AWS"):
                service_type = "left"
            elif service.startswith("Amazon"):
                service_type = "right"
            else:
                service_type = "bottom"
        else:  # ハードモード
            if self.play_mode == TIME_ATTACK:
                # ランダムにカテゴリを選択
                service_type = random.choice(["left", "right", "bottom"])
                # 選択したカテゴリからランダムにサービスを選択
                service = random.choice(hard_mode_services[service_type])
            else:
                # 全サービス仕分けモードでは残りのサービスから選択
                service = self.services_to_sort.pop(0)
                # サービスの種類を判定（ハードモードでは名前から判断する必要がある）
                if service in hard_mode_services["left"]:
                    service_type = "left"
                elif service in hard_mode_services["right"]:
                    service_type = "right"
                else:
                    service_type = "bottom"

        self.current_service = service
        self.current_type = service_type
        self.display_timer = 0
        self.result_display = None
        self.time_bonus_added = False  # 新しい問題ごとにリセット

    def process_key(self, key):
        """キー入力を処理する"""
        if self.result_display:  # 結果表示中は入力を無視
            return

        correct = False

        if key == pygame.K_LEFT and self.current_type == "left":
            correct = True
        elif key == pygame.K_RIGHT and self.current_type == "right":
            correct = True
        elif key == pygame.K_UP and self.current_type == "bottom":
            correct = True

        current_time = time.time()

        if correct:
            self.score += 10
            self.result_display = "正解！"
            self.feedback_symbol = "correct"  # ◯表示

            # コンボ処理
            if (
                self.last_answer_time > 0
                and (current_time - self.last_answer_time) <= self.answer_time_limit
            ):
                self.combo_count += 1
                # コンボボーナス（コンボ数に応じてスコア加算）
                combo_bonus = min(self.combo_count, 10)  # 最大10倍まで
                self.score += combo_bonus

                # 10コンボごとに5秒追加
                if (
                    self.play_mode == TIME_ATTACK
                    and self.combo_count > 0
                    and self.combo_count % 10 == 0
                ):
                    self.time_limit += 5  # 制限時間に5秒追加
                    self.time_bonus_added = True
                    self.result_display = "正解！ +5秒ボーナス！"
            else:
                self.combo_count = 1  # コンボリセットして1から

            if self.play_mode == COMPLETE_ALL:
                self.sorted_services += 1
        else:
            self.result_display = "不正解..."
            self.feedback_symbol = "incorrect"  # ×表示
            self.combo_count = 0  # コンボリセット
            self.mistakes += 1  # 間違いカウント

            # 不正解時のペナルティ：時間を即時に減らす
            if self.play_mode == TIME_ATTACK:
                self.time_limit -= 3  # 制限時間から3秒減少
                if self.time_limit <= 0:
                    self.game_over = True
                    return

        # 最後の回答時間を更新
        self.last_answer_time = current_time

        self.result_timer = 0
        self.symbol_timer = 0

        # 次のサービスを表示する前に少し待つ（不正解の場合は少し長く）
        if correct:
            pygame.time.delay(200)
        else:
            pygame.time.delay(500)  # 不正解の場合は少し長めに表示

        # 次のサービスへ
        if not self.game_over:
            self.next_service()

    def update(self):
        """ゲームの状態を更新する"""
        # 制限時間モードの場合、時間を更新
        if self.play_mode == TIME_ATTACK:
            if self.start_time is None:
                self.start_time = time.time()

            self.remaining_time = max(
                0, self.time_limit - (time.time() - self.start_time)
            )

            if self.remaining_time <= 0:
                self.game_over = True
                if self.end_time is None:
                    self.end_time = time.time()  # 終了時間を記録

        # 全サービスモードで全て仕分け終わったらゲーム終了
        if (
            self.play_mode == COMPLETE_ALL
            and self.sorted_services >= self.total_services
        ):
            self.game_over = True
            if self.end_time is None:
                self.end_time = time.time()  # 終了時間を記録

        # 結果表示のタイマーを更新
        if self.result_display:
            self.result_timer += 1
            if self.result_timer > 30:  # 約0.5秒表示
                self.result_display = None

        # シンボル表示のタイマーを更新
        if self.feedback_symbol:
            self.symbol_timer += 1
            if self.symbol_timer > 45:  # 約0.75秒表示
                self.feedback_symbol = None

        # コンボが続いているか確認（一定時間経過でリセット）
        if (
            self.combo_count > 0
            and time.time() - self.last_answer_time > self.answer_time_limit
        ):
            self.combo_count = 0

    def draw(self, screen):
        """ゲーム画面を描画する"""
        # 背景
        screen.fill(WHITE)

        # スコアとコンボ表示（上部）
        score_text = font_medium.render(f"スコア: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # モード表示
        difficulty_text = font_medium.render(
            f"難易度: {'ハード' if self.difficulty_mode == HARD_MODE else 'ノーマル'}",
            True,
            BLACK,
        )
        screen.blit(difficulty_text, (10, 40))

        play_mode_text = font_medium.render(
            f"モード: {'制限時間' if self.play_mode == TIME_ATTACK else '全サービス'}",
            True,
            BLACK,
        )
        screen.blit(play_mode_text, (10, 70))

        # コンボ表示（右上）- 虹色グラデーション
        if self.combo_count > 1:
            # コンボテキストを作成
            combo_text = f"{self.combo_count} COMBO!"

            # 虹色グラデーションでテキストを描画
            text_width = font_medium.size(combo_text)[0]
            char_width = text_width / len(combo_text)

            # 各文字の色を計算（虹色グラデーション）
            for i, char in enumerate(combo_text):
                # 色のインデックスを計算（時間によって変化）
                color_idx = (i + int(time.time() * 5)) % len(RAINBOW_COLORS)
                next_idx = (color_idx + 1) % len(RAINBOW_COLORS)

                # 2色間の補間
                ratio = (time.time() * 5) % 1.0
                r = int(
                    RAINBOW_COLORS[color_idx][0] * (1 - ratio)
                    + RAINBOW_COLORS[next_idx][0] * ratio
                )
                g = int(
                    RAINBOW_COLORS[color_idx][1] * (1 - ratio)
                    + RAINBOW_COLORS[next_idx][1] * ratio
                )
                b = int(
                    RAINBOW_COLORS[color_idx][2] * (1 - ratio)
                    + RAINBOW_COLORS[next_idx][2] * ratio
                )

                char_text = font_medium.render(char, True, (r, g, b))
                screen.blit(char_text, (WIDTH - text_width - 10 + i * char_width, 10))

            # コンボタイマー表示（残り時間バー）
            time_passed = time.time() - self.last_answer_time
            time_ratio = max(0, 1 - (time_passed / self.answer_time_limit))
            bar_width = 100 * time_ratio

            # 虹色のグラデーションバー
            for i in range(int(bar_width)):
                color_idx = (i * len(RAINBOW_COLORS) // 100) % len(RAINBOW_COLORS)
                pygame.draw.line(
                    screen,
                    RAINBOW_COLORS[color_idx],
                    (WIDTH - 110 + i, 40),
                    (WIDTH - 110 + i, 50),
                )

            pygame.draw.rect(screen, BLACK, (WIDTH - 110, 40, 100, 10), 1)  # 枠線

        # 制限時間モードの場合、残り時間を表示
        if self.play_mode == TIME_ATTACK:
            time_text = font_medium.render(
                f"残り時間: {int(self.remaining_time)}秒",
                True,
                RED if self.remaining_time < 10 else BLACK,
            )
            screen.blit(time_text, (10, 100))

            # 不正解数表示
            mistakes_text = font_small.render(
                f"不正解: {self.mistakes}回 (ペナルティ: -3秒/回)", True, BLACK
            )
            screen.blit(mistakes_text, (10, 130))

            # コンボボーナス説明
            combo_bonus_text = font_small.render(
                "10コンボごとに +5秒ボーナス", True, GREEN
            )
            screen.blit(combo_bonus_text, (10, 160))
        else:
            # 全サービスモードの場合、進捗と経過時間を表示
            progress_text = font_medium.render(
                f"進捗: {self.sorted_services}/{self.total_services}", True, BLACK
            )
            screen.blit(progress_text, (10, 100))

            elapsed_time = time.time() - self.start_time
            time_text = font_medium.render(
                f"経過時間: {int(elapsed_time)}秒", True, BLACK
            )
            screen.blit(time_text, (10, 130))

            # 不正解数表示
            mistakes_text = font_small.render(f"不正解: {self.mistakes}回", True, BLACK)
            screen.blit(mistakes_text, (10, 160))

        # 操作方法のリマインダー
        controls_text = font_small.render("← AWS | → Amazon | ↑ その他", True, BLACK)
        screen.blit(controls_text, (WIDTH - controls_text.get_rect().width - 10, 70))

        # 現在のサービス名を表示（ウィンドウの真ん中）
        if self.current_service:
            service_text = font_large.render(self.current_service, True, BLACK)
            screen.blit(
                service_text,
                (WIDTH // 2 - service_text.get_rect().width // 2, HEIGHT // 2 - 25),
            )

            # 矢印キーのヒント表示
            arrow_size = 50
            arrow_y = HEIGHT // 2 + 100  # サービス名の下に表示

            # 左矢印（AWS）
            pygame.draw.polygon(
                screen,
                BLUE,
                [
                    (WIDTH // 4 - arrow_size, arrow_y),
                    (WIDTH // 4, arrow_y - arrow_size // 2),
                    (WIDTH // 4, arrow_y + arrow_size // 2),
                ],
            )
            aws_text = font_small.render("AWS", True, BLACK)
            screen.blit(
                aws_text,
                (
                    WIDTH // 4 - aws_text.get_rect().width // 2,
                    arrow_y + arrow_size // 2 + 10,
                ),
            )

            # 右矢印（Amazon）
            pygame.draw.polygon(
                screen,
                ORANGE,
                [
                    (WIDTH * 3 // 4 + arrow_size, arrow_y),
                    (WIDTH * 3 // 4, arrow_y - arrow_size // 2),
                    (WIDTH * 3 // 4, arrow_y + arrow_size // 2),
                ],
            )
            amazon_text = font_small.render("Amazon", True, BLACK)
            screen.blit(
                amazon_text,
                (
                    WIDTH * 3 // 4 - amazon_text.get_rect().width // 2,
                    arrow_y + arrow_size // 2 + 10,
                ),
            )

            # 上矢印（その他）
            pygame.draw.polygon(
                screen,
                GREEN,
                [
                    (WIDTH // 2, arrow_y - arrow_size),
                    (WIDTH // 2 - arrow_size // 2, arrow_y),
                    (WIDTH // 2 + arrow_size // 2, arrow_y),
                ],
            )
            other_text = font_small.render("その他", True, BLACK)
            screen.blit(
                other_text,
                (WIDTH // 2 - other_text.get_rect().width // 2, arrow_y + 10),
            )

        # 結果表示（サービス名の上に表示）
        if self.result_display:
            result_color = (
                GREEN
                if self.result_display == "正解！" or "ボーナス" in self.result_display
                else RED
            )
            result_text = font_large.render(self.result_display, True, result_color)
            screen.blit(
                result_text,
                (WIDTH // 2 - result_text.get_rect().width // 2, HEIGHT // 2 - 80),
            )

        # ◯/×シンボル表示（サービス名の上に表示）
        if self.feedback_symbol:
            symbol_y = HEIGHT // 2 - 120  # サービス名よりさらに上

            if self.feedback_symbol == "correct":
                # 緑色の◯マーク
                pygame.draw.circle(screen, GREEN, (WIDTH // 2, symbol_y), 30)
                pygame.draw.circle(screen, WHITE, (WIDTH // 2, symbol_y), 25)
            else:
                # 赤色の×マーク
                pygame.draw.circle(screen, RED, (WIDTH // 2, symbol_y), 30)

                # バツ印
                line_width = 5
                pygame.draw.line(
                    screen,
                    WHITE,
                    (WIDTH // 2 - 15, symbol_y - 15),
                    (WIDTH // 2 + 15, symbol_y + 15),
                    line_width,
                )
                pygame.draw.line(
                    screen,
                    WHITE,
                    (WIDTH // 2 + 15, symbol_y - 15),
                    (WIDTH // 2 - 15, symbol_y + 15),
                    line_width,
                )
        # ゲームオーバー画面
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))

            if self.play_mode == TIME_ATTACK and self.remaining_time <= 0:
                game_over_text = font_large.render("時間切れ！", True, RED)
                screen.blit(
                    game_over_text,
                    (
                        WIDTH // 2 - game_over_text.get_rect().width // 2,
                        HEIGHT // 2 - 120,
                    ),
                )

                final_score_text = font_medium.render(
                    f"最終スコア: {self.score}", True, WHITE
                )
                screen.blit(
                    final_score_text,
                    (
                        WIDTH // 2 - final_score_text.get_rect().width // 2,
                        HEIGHT // 2 - 70,
                    ),
                )

                mistakes_text = font_medium.render(
                    f"不正解数: {self.mistakes}回", True, WHITE
                )
                screen.blit(
                    mistakes_text,
                    (
                        WIDTH // 2 - mistakes_text.get_rect().width // 2,
                        HEIGHT // 2 - 30,
                    ),
                )

                # 称号を表示
                for title_info in self.titles:
                    if self.score >= title_info["min_score"]:
                        title_text = font_large.render(
                            title_info["title"], True, title_info["color"]
                        )
                        screen.blit(
                            title_text,
                            (
                                WIDTH // 2 - title_text.get_rect().width // 2,
                                HEIGHT // 2 + 10,
                            ),
                        )
                        break

            elif (
                self.play_mode == COMPLETE_ALL
                and self.sorted_services >= self.total_services
            ):
                # 全サービス仕分け完了 - 時間を確実に停止
                if self.end_time is None:
                    self.end_time = time.time()

                elapsed_time = self.end_time - self.start_time
                minutes = int(elapsed_time) // 60
                seconds = int(elapsed_time) % 60

                # 全サービスモードではゲームオーバーではなく完了メッセージを表示
                complete_text = font_large.render("全サービス仕分け完了！", True, GREEN)
                screen.blit(
                    complete_text,
                    (
                        WIDTH // 2 - complete_text.get_rect().width // 2,
                        HEIGHT // 2 - 180,
                    ),
                )

                # リザルト画面のレイアウトを調整して画面内に収める
                time_text = font_medium.render(
                    f"所要時間: {minutes}分 {seconds}秒", True, WHITE
                )
                screen.blit(
                    time_text,
                    (WIDTH // 2 - time_text.get_rect().width // 2, HEIGHT // 2 - 130),
                )

                # 正解数と不正解数を明確に表示
                correct_answers = self.sorted_services - self.mistakes
                correct_text = font_medium.render(
                    f"正解数: {correct_answers}回", True, GREEN
                )
                screen.blit(
                    correct_text,
                    (WIDTH // 2 - correct_text.get_rect().width // 2, HEIGHT // 2 - 90),
                )

                mistakes_text = font_medium.render(
                    f"不正解数: {self.mistakes}回", True, RED
                )
                screen.blit(
                    mistakes_text,
                    (
                        WIDTH // 2 - mistakes_text.get_rect().width // 2,
                        HEIGHT // 2 - 50,
                    ),
                )

                # 正確率を計算して表示
                if self.sorted_services > 0:
                    accuracy = (correct_answers / self.sorted_services) * 100
                    accuracy_text = font_medium.render(
                        f"正確率: {accuracy:.1f}%", True, WHITE
                    )
                    screen.blit(
                        accuracy_text,
                        (
                            WIDTH // 2 - accuracy_text.get_rect().width // 2,
                            HEIGHT // 2 - 10,
                        ),
                    )

                # スコア表示
                final_score_text = font_medium.render(
                    f"最終スコア: {self.score}", True, WHITE
                )
                screen.blit(
                    final_score_text,
                    (
                        WIDTH // 2 - final_score_text.get_rect().width // 2,
                        HEIGHT // 2 + 30,
                    ),
                )

                # 称号を表示
                for title_info in self.titles:
                    if self.score >= title_info["min_score"]:
                        title_text = font_large.render(
                            title_info["title"], True, title_info["color"]
                        )
                        screen.blit(
                            title_text,
                            (
                                WIDTH // 2 - title_text.get_rect().width // 2,
                                HEIGHT // 2 + 70,
                            ),
                        )
                        break

                if self.mistakes == 0:
                    bonus_text = font_medium.render(
                        "ノーミスボーナス: +1000点", True, YELLOW
                    )
                    screen.blit(
                        bonus_text,
                        (
                            WIDTH // 2 - bonus_text.get_rect().width // 2,
                            HEIGHT // 2 + 110,
                        ),
                    )
                    self.score += 1000  # ノーミスボーナス
            else:
                game_over_text = font_large.render("ゲームオーバー", True, RED)
                screen.blit(
                    game_over_text,
                    (
                        WIDTH // 2 - game_over_text.get_rect().width // 2,
                        HEIGHT // 2 - 100,
                    ),
                )

            # 共通の終了画面要素
            restart_text = font_medium.render("Rキーで再スタート", True, WHITE)
            screen.blit(
                restart_text,
                (WIDTH // 2 - restart_text.get_rect().width // 2, HEIGHT // 2 + 150),
            )

            settings_text = font_medium.render("Sキーで設定画面", True, WHITE)
            screen.blit(
                settings_text,
                (WIDTH // 2 - settings_text.get_rect().width // 2, HEIGHT // 2 + 180),
            )

            quit_text = font_medium.render("Qキーで終了", True, WHITE)
            screen.blit(
                quit_text,
                (WIDTH // 2 - quit_text.get_rect().width // 2, HEIGHT // 2 + 210),
            )


# 設定画面
def show_settings_screen():
    """設定画面を表示し、選択された設定を返す"""
    difficulty_mode = NORMAL_MODE
    play_mode = TIME_ATTACK

    # タイトルアニメーション用の変数
    title_colors = [BLUE, ORANGE, GREEN]
    title_color_index = 0
    title_animation_timer = 0

    while True:
        screen.fill(WHITE)

        # タイトルアニメーション
        title_animation_timer += 1
        if title_animation_timer >= 30:  # 0.5秒ごとに色を変更
            title_animation_timer = 0
            title_color_index = (title_color_index + 1) % len(title_colors)

        # グラデーションタイトル背景
        title_bg = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
        for i in range(100):
            alpha = 100 - i  # 上から下に向かって透明になる
            pygame.draw.line(
                title_bg,
                (*title_colors[title_color_index][:3], alpha),
                (0, i),
                (WIDTH, i),
            )
        screen.blit(title_bg, (0, 30))  # 上部の余白を削除

        # タイトル
        title_shadow = font_large.render("AWS Service Sorter", True, (50, 50, 50))
        screen.blit(
            title_shadow, (WIDTH // 2 - title_shadow.get_rect().width // 2 + 2, 42)
        )

        title_text = font_large.render("AWS Service Sorter", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_rect().width // 2, 40))

        subtitle_text = font_medium.render(
            "クラウドマスターへの道", True, title_colors[title_color_index]
        )
        screen.blit(
            subtitle_text, (WIDTH // 2 - subtitle_text.get_rect().width // 2, 90)
        )

        # 難易度設定
        difficulty_title = font_medium.render("難易度:", True, BLACK)
        screen.blit(difficulty_title, (WIDTH // 2 - 200, 160))

        normal_rect = pygame.Rect(WIDTH // 2 - 80, 160, 120, 40)
        pygame.draw.rect(
            screen, BLUE if difficulty_mode == NORMAL_MODE else GRAY, normal_rect
        )
        normal_text = font_small.render(
            "ノーマル", True, WHITE if difficulty_mode == NORMAL_MODE else BLACK
        )
        screen.blit(
            normal_text,
            (
                normal_rect.centerx - normal_text.get_rect().width // 2,
                normal_rect.centery - normal_text.get_rect().height // 2,
            ),
        )

        hard_rect = pygame.Rect(WIDTH // 2 + 60, 160, 120, 40)
        pygame.draw.rect(
            screen, RED if difficulty_mode == HARD_MODE else GRAY, hard_rect
        )
        hard_text = font_small.render(
            "ハード", True, WHITE if difficulty_mode == HARD_MODE else BLACK
        )
        screen.blit(
            hard_text,
            (
                hard_rect.centerx - hard_text.get_rect().width // 2,
                hard_rect.centery - hard_text.get_rect().height // 2,
            ),
        )

        # プレイモード設定
        mode_title = font_medium.render("プレイモード:", True, BLACK)
        screen.blit(mode_title, (WIDTH // 2 - 200, 240))

        time_rect = pygame.Rect(WIDTH // 2 - 80, 240, 120, 40)
        pygame.draw.rect(screen, BLUE if play_mode == TIME_ATTACK else GRAY, time_rect)
        time_text = font_small.render(
            "制限時間", True, WHITE if play_mode == TIME_ATTACK else BLACK
        )
        screen.blit(
            time_text,
            (
                time_rect.centerx - time_text.get_rect().width // 2,
                time_rect.centery - time_text.get_rect().height // 2,
            ),
        )

        complete_rect = pygame.Rect(WIDTH // 2 + 60, 240, 120, 40)
        pygame.draw.rect(
            screen, GREEN if play_mode == COMPLETE_ALL else GRAY, complete_rect
        )
        complete_text = font_small.render(
            "全サービス", True, WHITE if play_mode == COMPLETE_ALL else BLACK
        )
        screen.blit(
            complete_text,
            (
                complete_rect.centerx - complete_text.get_rect().width // 2,
                complete_rect.centery - complete_text.get_rect().height // 2,
            ),
        )

        # 説明
        if difficulty_mode == NORMAL_MODE:
            diff_desc = "「AWS」「Amazon」の接頭辞ありでサービス名が表示されます"
        else:
            diff_desc = "接頭辞なしでサービス名が表示されます（難しい）"
        diff_desc_text = font_small.render(diff_desc, True, BLACK)
        screen.blit(
            diff_desc_text, (WIDTH // 2 - diff_desc_text.get_rect().width // 2, 210)
        )

        if play_mode == TIME_ATTACK:
            mode_desc = "60秒間でいくつのサービスを正しく仕分けられるか挑戦します"
        else:
            mode_desc = "全てのAWSサービスを仕分けるまで続きます"
        mode_desc_text = font_small.render(mode_desc, True, BLACK)
        screen.blit(
            mode_desc_text, (WIDTH // 2 - mode_desc_text.get_rect().width // 2, 290)
        )

        # 操作説明
        controls_text = font_small.render(
            "矢印キーで仕分け: ← AWS | → Amazon | ↑ その他", True, BLACK
        )
        screen.blit(
            controls_text, (WIDTH // 2 - controls_text.get_rect().width // 2, 340)
        )

        # スタートボタン
        start_rect = pygame.Rect(WIDTH // 2 - 100, 400, 200, 60)

        # ボタンのグラデーション効果
        for i in range(60):
            color = (0, min(255, 180 + i * 1.25), 0)  # 緑色のグラデーション
            pygame.draw.rect(
                screen, color, pygame.Rect(start_rect.x, start_rect.y + i, 200, 1)
            )

        # ボタンの枠線
        pygame.draw.rect(screen, BLACK, start_rect, 2)

        start_text = font_medium.render("ゲーム開始", True, WHITE)
        screen.blit(
            start_text,
            (
                start_rect.centerx - start_text.get_rect().width // 2,
                start_rect.centery - start_text.get_rect().height // 2,
            ),
        )

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # 難易度選択
                if normal_rect.collidepoint(mouse_pos):
                    difficulty_mode = NORMAL_MODE
                elif hard_rect.collidepoint(mouse_pos):
                    difficulty_mode = HARD_MODE

                # プレイモード選択
                if time_rect.collidepoint(mouse_pos):
                    play_mode = TIME_ATTACK
                elif complete_rect.collidepoint(mouse_pos):
                    play_mode = COMPLETE_ALL

                # ゲーム開始
                if start_rect.collidepoint(mouse_pos):
                    return difficulty_mode, play_mode

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        pygame.time.Clock().tick(60)


# ゲームのメインループ
def main():
    clock = pygame.time.Clock()

    # 最初は設定画面を表示
    difficulty_mode, play_mode = show_settings_screen()
    game_state = GameState(difficulty_mode, play_mode)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_r and game_state.game_over:
                    # 同じ設定で再スタート
                    game_state = GameState(difficulty_mode, play_mode)

                if event.key == pygame.K_s and game_state.game_over:
                    # 設定画面に戻る
                    difficulty_mode, play_mode = show_settings_screen()
                    game_state = GameState(difficulty_mode, play_mode)

                # ゲームプレイ中の矢印キー入力
                if not game_state.game_over and event.key in [
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_UP,
                ]:
                    game_state.process_key(event.key)

        # ゲームの更新
        if not game_state.game_over:
            game_state.update()

        # 描画
        game_state.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
