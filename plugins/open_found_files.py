import sublime
import sublime_plugin

# Related reading:
#     http://stackoverflow.com/questions/40088877/sublime-text-open-all-files-containing-search-term

# This adds a new command named "open_all_found_files" which can be bound to a
# key, added to the command palette, etc. When you invoke the command while
# inside of the results of a "Find in Files" operation it will locate all of
# the filenames where matches were found and open them.
#
# The command takes an optional parameter "new_window" which you can pass and
# set to true if you want the results to open in a new window; otherwise they
# open in the current window.
#
# To add this to the command palette, create a sublime-commands file that
# contains the following in your User package, or add the commands to an
# existing file if you have one; use 'Preferences > Browse Packages' to find
# the location if you don't know where it is.
#
# [
#     {
#         "caption": "Find in Files: Open Matching Files",
#         "command": "open_all_found_files"
#     },
#     {
#         "caption": "Find in Files: Open Matching Files in New Window",
#         "command": "open_all_found_files",
#         "args": {
#             "new_window": true
#         }
#     },
# ]

class OpenAllFoundFilesCommand(sublime_plugin.TextCommand):
    """
    Collect the names of all files from a Find in Files result and open them
    all at once, optionally in a new window.
    """
    def run(self, edit, new_window=False):
        # Collect all found filenames
        positions = self.view.find_by_selector("entity.name.filename.find-in-files")
        if len(positions) > 0:
            # Set up the window to open the files in
            if new_window:
                sublime.run_command("new_window")
                window = sublime.active_window()
            else:
                window = self.view.window()

            # Open each file in the new window
            for position in positions:
                window.run_command('open_file', {'file': self.view.substr (position)})
        else:
            self.view.window().status_message("No find results")

    def is_enabled(self):
        return self.view.match_selector(0, "text.find-in-files")
