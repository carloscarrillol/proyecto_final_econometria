import os
import csv
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Cargar la clave API
load_dotenv()
key = os.getenv('API_KEY')

# Inicializar cliente de la API de YouTube
youtube = build(
    serviceName='youtube',
    version='v3',
    developerKey=key
)

# Obtener el channelId del canal 'Unik Jane'
request_id = youtube.search().list(
    part='snippet',
    q='Unik Jane',
    type='channel',
    maxResults=1
)
response_id = request_id.execute()
unik_id = response_id['items'][0]['id']['channelId']

# Obtener los últimos 5 videos del canal
request_uploads = youtube.search().list(
    part='snippet',
    channelId=unik_id,
    maxResults=5,
    order='date',
    type='video'
)
response_uploads = request_uploads.execute()
video_items = response_uploads['items']

# Extraer los IDs de los 5 videos
video_ids = [item['id']['videoId'] for item in video_items]

# Lista donde se guardarán los datos
comments_data = []

# Recorrer los videos y extraer los comentarios
for video_id in video_ids:
    request_comments = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=10,
        textFormat='plainText'
    )
    response_comments = request_comments.execute()
    for item in response_comments.get('items', []):
        comment_id = item['id']
        text = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments_data.append([comment_id, text, video_id])

# Guardar en un CSV
output_path = 'data/dataset.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['comment_id', 'text', 'video_id'])  # encabezado
    writer.writerows(comments_data)
