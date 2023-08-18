# hosnakpub
ほしのなか政府の広報サイト

## 開発環境
### 環境構築
- `.env.sample`を`.env`として、適切に編集してください
- `DEBUG=True`です

### コンテナのビルド
`docker compose build`

### コンテナの起動
`docker compose up`

### コンテナの削除
`docker compose down`

## ステージング環境
### 環境構築
- `.env.sample`を`.env.staging`として、適切に編集してください
- `DEBUG=True`です

### コンテナのビルド
`docker compose -f docker-compose.staging.yml build`

### コンテナの起動
`docker compose -f docker-compose.staging.yml up`

### コンテナの削除
`docker compose -f docker-compose.staging.yml down`

## 本番環境
### 環境構築
- `.env.sample`を`.env.prod`として適切に編集してください
- **コンテナをビルドする前**に、サーバー内で、`docker-compose.prod.yml`の`https-portal: environment: STAGE`の記述を除去して、SSLが適切に取得できるかを確認してください
    - 確認が完了したら記述を戻してください

### コンテナのビルド
`docker compose -f docker-compose.prod.yml build`

### コンテナの起動
`docker compose -f docker-compose.prod.yml up`

### コンテナの削除
`docker compose -f docker-compose.prod.yml down`
