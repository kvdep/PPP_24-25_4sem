from fastapi import FastAPI
from app.api.visualise import router as vis_router
from app.api.graph import router as graph_router

app = FastAPI()
#app.include_router(scrape_router, prefix="/scrape", tags=["Scraping"])
app.include_router(graph_router, prefix="/graph", tags=["Graph"])
app.include_router(vis_router, prefix="/vis", tags=["Visualise"])

def main():
    pass

if __name__ == "__main__":
    main()

