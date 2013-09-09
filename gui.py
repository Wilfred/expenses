import sys

from gi.repository import Gtk

from print_expenses import parse_csv


class CellRendererTextWindow(Gtk.Window):

    def __init__(self, rows):
        Gtk.Window.__init__(self, title="CellRendererText Example")

        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(object, str, float)
        for row in rows:
            self.liststore.append(row)

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_date = Gtk.CellRendererText()
        column_date = Gtk.TreeViewColumn("Date", renderer_date, text=0)
        treeview.append_column(column_date)

        renderer_desc = Gtk.CellRendererText()
        column_desc = Gtk.TreeViewColumn("Description", renderer_desc, text=1)
        treeview.append_column(column_desc)

        renderer_amount = Gtk.CellRendererText()
        column_amount = Gtk.TreeViewColumn("Amount", renderer_amount, text=0)
        treeview.append_column(column_amount)

        self.add(treeview)

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python print_expenses.py /path/to/csv"
        sys.exit(1)
    else:
        file_name = sys.argv[-1]
        
    rows = parse_csv(file_name)

    win = CellRendererTextWindow(rows)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
