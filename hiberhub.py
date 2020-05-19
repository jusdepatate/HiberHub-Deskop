#!/usr/bin/env python3
# HiberHub-Desktop - GTK-based desktop client for Hiber services.
# Jus de Patate_ - 2020
import os
from urllib.parse import urlparse, unquote
from base64 import b64decode

try:
    import requests
except ImportError:
    print("Couldn't import requests, did you install all required Pip packages ?")

try:
    import gi

    gi.require_version("Gtk", "3.0")
    gi.require_version("Notify", "0.7")
    from gi.repository import Gtk, Gdk, Notify, GdkPixbuf
except ImportError:
    print("Couldn't import PYGObject, is it installed ? ?")

hiberlink = "https://hiber.link"
hiberfile = "https://hiberfile.com"
# as both are open source anyone can make have his very own instance so main url is editable


class HiberHub(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="HiberHub", resizable=False)
        Notify.init("HiberHub")

        icon = "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"

        # HiberHub's icon a bit modified, in 194x194 and in b64

        self.connect("drag_data_received", self.onDrag)
        self.drag_dest_set(
            Gtk.DestDefaults.MOTION
            | Gtk.DestDefaults.HIGHLIGHT
            | Gtk.DestDefaults.DROP,
            [Gtk.TargetEntry.new("text/uri-list", 0, 80)],
            Gdk.DragAction.COPY,
        )
        self.set_resizable(False)

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(self.box)

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        self.hiberlinkButton = Gtk.Button(label="HiberLink")
        self.hiberlinkButton.connect("clicked", self.shortLink)

        self.hiberfileButton = Gtk.Button(label="HiberFile")
        self.hiberfileButton.connect("clicked", self.uploadFile)

        self.box.pack_start(self.hiberlinkButton, True, True, 0)
        self.box.pack_start(self.hiberfileButton, True, True, 0)

    def shortLink(self, widget):
        originalLink = self.pasteText()
        if originalLink is not None:
            r = requests.post(
                hiberlink + "/link.php",
                data={"link": originalLink},
                headers={"User-Agent": "curl"},
            )
            shortLinkk = r.text

            if shortLinkk == "erreur":
                Notify.Notification.new(
                    "HiberHub", "HiberLink: Couldn't reduce link"
                ).show()
            else:
                self.copyText(r.text)
                Notify.Notification.new(
                    "HiberHub", "HiberLink: Short link has been copied"
                ).show()
        else:
            Notify.Notification.new(
                "HiberHub", "HiberLink: No text in the clipboard detected"
            ).show()

            return "error"

    def uploadFile(self, widget):
        if not widget:
            file = self.pasteText()
        else:
            dlg = Gtk.FileChooserDialog(
                "HiberHub - Open",
                self,
                Gtk.FileChooserAction.OPEN,
                (
                    Gtk.STOCK_CANCEL,
                    Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN,
                    Gtk.ResponseType.OK,
                ),
            )
            dlg.run()
            file = dlg.get_filename()
            dlg.destroy()

        fileDict = {"my_file": open(file, "rb")}

        Notify.Notification.new("HiberHub", "HiberFile: Uploading...").show()

        try:
            r = requests.post(
                hiberfile + "/send.php", files=fileDict, data={"time": "7 jours"}
            )
        except requests.exceptions:
            Notify.Notification.new("HiberHub", "HiberFile: File upload failed").show()
            return

        fileLink = r.headers["X-HIBERFILE-LINK"]

        if fileLink == "Erreur":
            Notify.Notification.new("HiberHub", "HiberFile: File upload failed").show()
        else:
            self.copyText(fileLink)
            Notify.Notification.new(
                "HiberHub", "HiberFile: File link has been copied"
            ).show()

    def onDrag(self, widget, context, x, y, selection, target_type, timestamp):
        if target_type == 80:
            uri = selection.get_data()

            filePath = urlparse(uri)
            filePath = str(
                os.path.abspath(os.path.join(filePath.netloc, filePath.path))
            )[:-5][2:]
            filePath = unquote(filePath)

            self.copyText(filePath)
            self.uploadFile(False)

    def copyText(self, text):
        self.clipboard.set_text(text, -1)

    def pasteText(self):
        text = self.clipboard.wait_for_text()
        if text is not None:
            return text
        else:
            return ""


win = HiberHub()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
