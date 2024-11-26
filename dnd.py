import pythoncom
import win32api
import win32con
import win32gui
import win32com.server.policy
import win32com.shell.shell as shell
from ctypes import windll, create_unicode_buffer
import flet as ft
import threading
import time
import queue
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DROPEFFECT_NONE = 0
DROPEFFECT_COPY = 1
DROPEFFECT_MOVE = 2
DROPEFFECT_LINK = 4

class IDropTarget(win32com.server.policy.DesignatedWrapPolicy):
    _com_interfaces_ = [pythoncom.IID_IDropTarget]
    _public_methods_ = ['DragEnter', 'DragOver', 'DragLeave', 'Drop']

    def __init__(self, callback):
        self._wrap_(self)
        self.callback = callback
        logger.debug("IDropTarget initialized")

    def DragEnter(self, pDataObj, grfKeyState, point_tuple, pdwEffect):
        logger.debug("DragEnter called")
        try:
            # Create format structure using native COM objects
            format = (
                win32con.CF_HDROP,        # Format
                None,                     # Target device
                pythoncom.DVASPECT_CONTENT,  # Aspect
                -1,                       # Index
                pythoncom.TYMED_HGLOBAL   # Storage medium
            )
            
            # Try to get the data
            try:
                pDataObj.QueryGetData(format)
                return DROPEFFECT_COPY
            except:
                return DROPEFFECT_NONE
        except Exception as e:
            logger.exception("Error in DragEnter")
            return DROPEFFECT_NONE

    def DragOver(self, grfKeyState, point_tuple, pdwEffect):
        logger.debug("DragOver called")
        return DROPEFFECT_COPY

    def DragLeave(self):
        logger.debug("DragLeave called")
        return DROPEFFECT_NONE

    def Drop(self, pDataObj, grfKeyState, point_tuple, pdwEffect):
        logger.debug("Drop called")
        try:
            format = (
                win32con.CF_HDROP,
                None,
                pythoncom.DVASPECT_CONTENT,
                -1,
                pythoncom.TYMED_HGLOBAL
            )

            medium = pDataObj.GetData(format)
            
            if medium.data:
                # Get file count
                file_count = windll.shell32.DragQueryFileW(medium.data, -1, None, 0)
                logger.debug(f"Number of files dropped: {file_count}")
                
                # Get all filenames
                files = []
                for i in range(file_count):
                    length = windll.shell32.DragQueryFileW(medium.data, i, None, 0) + 1
                    buffer = create_unicode_buffer(length)
                    windll.shell32.DragQueryFileW(medium.data, i, buffer, length)
                    files.append(buffer.value)
                    logger.debug(f"File {i}: {buffer.value}")

                self.callback(files)
                return DROPEFFECT_COPY
            
            return DROPEFFECT_NONE
            
        except Exception as e:
            logger.exception("Error in Drop")
            return DROPEFFECT_NONE

class DropTarget:
    def __init__(self, hwnd, callback):
        self.hwnd = hwnd
        self.callback = callback
        self.running = True
        
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        logger.debug(f"DropTarget initialized for window handle: {hwnd}")

    def _run(self):
        try:
            logger.debug("COM thread starting")
            pythoncom.OleInitialize()
            
            logger.debug("Creating drop target")
            drop_target = IDropTarget(self.callback)
            drop_target_ptr = pythoncom.WrapObject(
                drop_target, pythoncom.IID_IDropTarget, pythoncom.IID_IDropTarget
            )
            
            logger.debug("Registering drop target")
            result = pythoncom.RegisterDragDrop(self.hwnd, drop_target_ptr)
            logger.debug(f"RegisterDragDrop result: {result}")
            
            logger.debug("Starting message pump")
            while self.running:
                pythoncom.PumpMessages()
                
        except Exception as e:
            logger.exception("Error in drop target thread")
        finally:
            try:
                logger.debug("Cleaning up COM resources")
                pythoncom.RevokeDragDrop(self.hwnd)
                pythoncom.CoUninitialize()
            except Exception as e:
                logger.exception("Error during cleanup")

    def stop(self):
        logger.debug("Stopping drop target")
        self.running = False
        win32gui.PostThreadMessage(self.thread.ident, win32con.WM_QUIT, 0, 0)
        self.thread.join()

def find_window_by_title(title):
    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            lParam.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(enum_windows_proc, hwnds)
    hwnd = hwnds[0] if hwnds else None
    logger.debug(f"Found window handle for '{title}': {hwnd}")
    return hwnd

def main(page: ft.Page):
    page.title = "Drag and Drop Demo"
    logger.debug("Application starting")
    
    files_container = ft.Column(scroll=ft.ScrollMode.AUTO)
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Drag and Drop Files Here", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                files_container
            ]),
            padding=20,
            border=ft.border.all(2, ft.colors.BLUE_200),
            border_radius=10,
            expand=True
        )
    )

    def handle_drop(files):
        logger.debug(f"Handling drop of {len(files)} files")
        def update_ui():
            files_container.controls.clear()
            for file in files:
                files_container.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.FILE_PRESENT),
                        title=ft.Text(file)
                    )
                )
            page.update()
        page.run_thread(update_ui)

    drop_target = None
    def on_window_handle_found(hwnd):
        nonlocal drop_target
        if hwnd:
            logger.debug(f"Creating drop target for window {hwnd}")
            drop_target = DropTarget(hwnd, handle_drop)

    threading.Thread(
        target=lambda: poll_for_window_handle(page.title, on_window_handle_found),
        daemon=True
    ).start()

    def on_close():
        if drop_target:
            drop_target.stop()

    page.on_close = on_close
    page.update()

def poll_for_window_handle(title, callback):
    hwnd = None
    while hwnd is None:
        hwnd = find_window_by_title(title)
        time.sleep(0.1)
    callback(hwnd)

if __name__ == "__main__":
    ft.app(target=main)