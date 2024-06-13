import os
import shutil
from PIL import Image
import subprocess
from pathlib import Path
import threading

try:
    import ctypes
except ImportError:
    print("ctypes not available. If you are on Windows install it")
try:
    from AppKit import NSImage, NSWorkspace, NSURL
    from Cocoa import NSData
except ImportError:
    print("AppKit not available. If you are on macOS install them")
try:
    from gi import require_version

    require_version("Gtk", "3.0")
    from gi.repository import Gtk
except ImportError:
    print("Gtk not available. If you are on Linux install it")

import flet as ft
from flet.version import version as flet_version
from flet_runtime.utils import is_macos, is_windows, is_linux


class change_app_icon:
    def __init__(self, icon_path, app_name=None, app_path=None):
        self.image_path = os.path.abspath(icon_path)
        self.icon_path = self.get_icon_path()
        self.app_name = app_name
        self.app_path = (
            app_path
            if app_path
            else Path.home().joinpath(
                ".flet",
                "bin",
                f"flet-{flet_version}",
                f"{app_name}.app" if self.app_name else "Flet.app",
            )
        )
        self._change_app_icon()

    def get_icon_path(self):
        image_type = self.get_image_type(self.image_path)
        print(image_type)
        if image_type not in ["ico", "png", "jpeg", "bmp", "icns"]:
            raise ValueError(f"Unsupported image type: {image_type}")

        if image_type != "ico" and is_windows():
            # Convert to ICO if the image is not already in ICO format
            base, _ = os.path.splitext(self.image_path)
            ico_path = f"{base}.ico"
            self.convert_png_to_ico(self.image_path, ico_path)
            return ico_path
        elif is_macos() and image_type != "icns":
            # Convert to ICNS if the image is not already in ICNS format for macOS
            icns_path = "/tmp/new_icon.icns"
            self.convert_png_to_icns(self.image_path, icns_path)
            return icns_path
        return self.image_path

    @staticmethod
    def get_image_type(image_path):
        with Image.open(image_path) as img:
            return img.format.lower()

    @staticmethod
    def convert_png_to_ico(png_path, ico_path):
        img = Image.open(png_path)
        img.save(
            ico_path, format="ICO", sizes=[(32, 32), (64, 64), (128, 128), (256, 256)]
        )

    @staticmethod
    def convert_png_to_icns(png_path, icns_path):
        iconset_dir = "/tmp/icon.iconset"
        os.makedirs(iconset_dir, exist_ok=True)

        sizes = [16, 32, 128, 256, 512]
        for size in sizes:
            img = Image.open(png_path)
            img.resize((size, size)).save(f"{iconset_dir}/icon_{size}x{size}.png")
            img.resize((size * 2, size * 2)).save(
                f"{iconset_dir}/icon_{size}x{size}@2x.png"
            )

        subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", icns_path])
        shutil.rmtree(iconset_dir)

    def _change_app_icon(self):
        if is_windows():
            threading.Thread(target=self._change_app_icon_windows).start()
        elif is_macos():
            self._change_app_icon_macos()
        elif is_linux():
            self._change_app_icon_linux()
        else:
            raise Exception(f"Unsupported OS: {system}")

    def _change_app_icon_windows(self):
        import pygetwindow as gw

        def perform_change():
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            IDI_APPLICATION = 32512
            WM_SETICON = 0x0080
            ICON_SMALL = 0
            ICON_BIG = 1

            hicon = user32.LoadImageW(
                0, self.icon_path, 1, 0, 0, 0x00000010 | 0x00000002
            )
            if not hicon:
                raise Exception(
                    f"Failed to load icon: {ctypes.WinError(ctypes.get_last_error())}"
                )

            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                raise Exception(
                    f"Failed to get foreground window: {ctypes.WinError(ctypes.get_last_error())}"
                )

            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)

            kernel32.CloseHandle(hicon)

        # check for the creation of the flet window before changing the icon
        while True:
            windows = gw.getWindowsWithTitle(self.app_name)
            if windows:
                perform_change()
                break

    def _change_app_icon_macos(self):
        if not os.path.exists(self.app_path):
            print(f"Error: '{self.app_path}' does not exist.")
            return
        if not os.path.exists(self.icon_path):
            print(f"Error: '{self.icon_path}' does not exist.")
            return

        # Remove the "Icon^M" file if it exists
        self.remove_icon_cr()

        try:
            new_icon_dest_path = os.path.join(
                self.app_path, "Contents", "Resources", "new_icon.icns"
            )
            shutil.copy(self.icon_path, new_icon_dest_path)
        except Exception as e:
            print(f"Error copying icon file: {e}")
            return

        self.modify_plist()

        # Create the "Icon^M" file with the correct resource fork data
        self.create_icon_cr(new_icon_dest_path)

        print(f"Icon successfully changed for '{self.app_path}'.")

    def modify_plist(self):
        plist_path = os.path.join(self.app_path, "Contents", "Info.plist")
        try:
            with open(plist_path, "r") as plist_file:
                plist_content = plist_file.read()

            if "new_icon.icns" not in plist_content:
                plist_content = plist_content.replace(
                    "<key>CFBundleIconFile</key><string>AppIcon</string>",
                    "<key>CFBundleIconFile</key><string>new_icon</string>",
                )

            with open(plist_path, "w") as plist_file:
                plist_file.write(plist_content)
        except Exception as e:
            print(f"Error modifying Info.plist: {e}")

    def remove_icon_cr(self):
        icon_cr_path = os.path.join(self.app_path, "Icon\r")
        if os.path.exists(icon_cr_path):
            try:
                os.remove(icon_cr_path)
                # print(f"Removed {icon_cr_path}")
            except Exception as e:
                print(f"Error removing 'Icon\r': {e}")

    def create_icon_cr(self, icns_path):
        icon_cr_path = os.path.join(self.app_path, "Icon\r")
        try:
            open(icon_cr_path, "a").close()  # empty file with the name 'Icon\r'
            app_url = NSURL.fileURLWithPath_(str(self.app_path))
            icon_url = NSURL.fileURLWithPath_(str(icns_path))
            icon_image = NSImage.alloc().initWithContentsOfURL_(icon_url)
            ws = NSWorkspace.sharedWorkspace()
            ws.setIcon_forFile_options_(icon_image, app_url.path(), 0)
            # print(f"Created {icon_cr_path}")
        except Exception as e:
            print(f"Error creating 'Icon\r': {e}")

    def _change_app_icon_linux(self):
        screen = Gtk.IconTheme.get_default()
        icon = Gtk.Image.new_from_file(self.icon_path)
        Gtk.Window.set_default_icon_list(icon.get_pixbuf())
