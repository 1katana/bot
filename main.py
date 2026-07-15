

from app.managers.solana_manager import SolanaManager
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop
import asyncio
from app.ui.main_ui import MainWindow



async def main():
    solana_manager = await SolanaManager.create()

    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow(solana_manager)
    window.show()
    
    with loop:
        await loop.run_forever()
        if window.close():
            loop.close()

if __name__ == "__main__":
    asyncio.run(main())
    

