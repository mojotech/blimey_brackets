import sublime, sublime_plugin, string

class ShowMatchingBracket(sublime_plugin.EventListener):

  def max_end(self, region_set):
    maximum = region_set[0].end()
    for r in region_set:
      if r.end() > maximum:
        maximum = r.end()
    return maximum

  def find_matching_bracket(self, cursor_loc, view):
    start_brackets = ['{']
    end_brackets = ['}']
    end_stack = []
    check_loc = cursor_loc - 1
    if view.substr(cursor_loc) in end_brackets:
      end_stack.append(view.substr(cursor_loc))
    while len(end_stack) > 0 and check_loc >= 0:
      check_char = view.substr(check_loc)
      # Check the score selector values
      if check_char in start_brackets:
        peek = end_stack[len(end_stack) - 1]
        if start_brackets.index(check_char) == end_brackets.index(peek):
          end_stack.pop()
      elif check_char in end_brackets:
        end_stack.append(check_char)
      check_loc -= 1
    if len(end_stack) == 0:
      return check_loc + 1
    else:
      return cursor_loc

  def on_selection_modified(self, view):
    end_brackets = ['}']
    cursor_loc = self.max_end(view.sel()) - 1
    previous_char = view.substr(cursor_loc)
    if previous_char in end_brackets:
      begin_loc = self.find_matching_bracket(cursor_loc, view)
      if begin_loc < cursor_loc:
        line = view.line(begin_loc)
        region = sublime.Region(line.begin(), begin_loc)
        match = view.substr(region).strip()
        sublime.status_message(match)
        view.add_regions('blimey_begin_bracket', [region], 'blimey_start', 'dot', sublime.HIDDEN)
        view.add_regions('blimey_end_bracket', [sublime.Region(cursor_loc, cursor_loc)], 'blimey_end', 'dot', sublime.HIDDEN)
      else:
        sublime.status_message('')
    else:
      view.erase_regions('blimey_begin_bracket')
      view.erase_regions('blimey_end_bracket')
