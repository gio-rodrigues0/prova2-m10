from fastapi import FastAPI, HTTPException
from logging_config import LoggerSetup
import logging
from typing import List, Optional
from schema import TSSongs

# Cria um logger raiz
logger_setup = LoggerSetup()

# Adiciona o logger para o módulo
LOGGER = logging.getLogger(__name__)

app = FastAPI()

songs: List[TSSongs] = []

@app.post("/songs/", response_model=TSSongs)
def create_song(song: TSSongs):
    songs.append(song)
    LOGGER.info(f"Música da Taylor adicionada com sucesso")
    return song

@app.get("/songs/", response_model=List[TSSongs])
def read_songs(album: Optional[str] = None):
    if album:
        LOGGER.info(f"Listando músicas da era {album} salvas")
        return [song for song in songs if song.album == album]
    LOGGER.info(f"Listando músicas da Taylor salvas")
    return songs

@app.get("/songs/{song_id}", response_model=TSSongs)
def read_song(song_id: int):
    for song in songs:
        if song.id == song_id:
            LOGGER.info(f"Retornando a música de id {song_id}")
            return song
    LOGGER.error(f"Não foi possível encontrar a música de id {song_id}")
    raise HTTPException(status_code=404, detail="Song not found")

@app.put("/songs/{song_id}", response_model=TSSongs)
def update_song(song_id: int, updated_song: TSSongs):
    for index, song in enumerate(songs):
        if song.id == song_id:
            songs[index] = updated_song
            LOGGER.info(f"Música de id {song_id} editada com sucesso")
            return updated_song
    LOGGER.error(f"Música de id {song_id} não encontrada")
    raise HTTPException(status_code=404, detail="Song not found")

@app.delete("/songs/{song_id}", response_model=TSSongs)
def delete_song(song_id: int):
    for index, song in enumerate(songs):
        if song.id == song_id:
            deleted_song = songs.pop(index)
            LOGGER.info(f"Música de id {song_id} deletada com sucesso")
            return deleted_song
    LOGGER.error(f"Música de id {song_id} não econtrada")
    raise HTTPException(status_code=404, detail="Song not found")

