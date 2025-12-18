import wx
import time

# =====================================================================
# ====================== GLOBAL GAME STATS ============================
# =====================================================================

game_start_time = None
total_mistakes = 0

def add_mistake():
    global total_mistakes
    total_mistakes += 1
    
# =====================================================================
# ========================= SHARED HELPERS =============================
# =====================================================================

def caesar_cipher(text, shift, mode='decrypt'):
    text = text.upper()
    out = ""
    A = 65
    for ch in text:
        if 'A' <= ch <= 'Z':
            idx = ord(ch) - A
            if mode == "decrypt":
                new = (idx - shift) % 26
            else:
                new = (idx + shift) % 26
            out += chr(new + A)
        else:
            out += ch
    return out


def hex_to_full_binary(hex_str, total_bits):
    return bin(int(hex_str, 16))[2:].zfill(total_bits)


def hacker_text(widget, size=12, color="CYAN"):
    neon = { "CYAN": wx.Colour(0, 255, 255), "MAGENTA": wx.Colour(255, 0, 255),  "YELLOW": wx.Colour(255, 255, 0),  "GREEN": wx.Colour(0, 255, 0),}
    widget.SetForegroundColour(neon[color])
    widget.SetBackgroundColour(wx.Colour(8, 8, 20))
    widget.SetFont(wx.Font(size, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

def hacker_button(button, color="MAGENTA"):
    neon = { "CYAN": wx.Colour(0, 255, 255), "MAGENTA": wx.Colour(255, 0, 255), "YELLOW": wx.Colour(255, 255, 0), "GREEN": wx.Colour(0, 255, 0),}
    button.SetBackgroundColour(wx.Colour(30, 0, 30))
    button.SetForegroundColour(neon[color])
    button.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

# =====================================================================
# ======================== START MENU SCREEN ==========================
# =====================================================================

def start_menu():
    frame = wx.Frame(None, title="🔐 Escape Room – Start", size=(500, 300))
    panel = wx.Panel(frame)
    panel.SetBackgroundColour(wx.Colour(10, 10, 25))
    title = wx.StaticText(panel, label="🔓 ULTIMATE ESCAPE ROOM 🔓")
    title.SetFont(wx.Font(20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    title.SetForegroundColour(wx.Colour(0, 200, 255))
    play_btn = wx.Button(panel, label="PLAY")
    exit_btn = wx.Button(panel, label="EXIT")
    hacker_button(play_btn, "GREEN")
    hacker_button(exit_btn, "MAGENTA")
    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 30)
    vbox.Add(play_btn, 0, wx.ALIGN_CENTER | wx.TOP, 40)
    vbox.Add(exit_btn, 0, wx.ALIGN_CENTER | wx.TOP, 20)
    panel.SetSizer(vbox)

    def start_game(event):
        frame.Close()
        global game_start_time
        game_start_time = time.time()
        room1(None)

    def exit_game(event):
        frame.Close()

    play_btn.Bind(wx.EVT_BUTTON, start_game)
    exit_btn.Bind(wx.EVT_BUTTON, exit_game)

    frame.Show()

# =====================================================================
# ======================= ROOM 4 SYMBOL CIPHER =========================
# =====================================================================

charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

def caesar_decrypt_symbol(text, shift):
    out = ""
    for ch in text:
        if ch in charset:
            idx = charset.index(ch)
            out += charset[(idx - shift) % len(charset)]
        else:
            out += ch
    return out

# Room 4 Q1
correct_1 = "MISSION2025!"
shift_1 = 5
enc1 = "".join(charset[(charset.index(c)+shift_1) % len(charset)] if c in charset else c
               for c in correct_1)

# Room 4 Q2
correct_2 = "GALAXY#42"
shift_2 = 7
enc2 = "".join(charset[(charset.index(c)+shift_2) % len(charset)] if c in charset else c
               for c in correct_2)

# =====================================================================
# ======================= FINAL ESCAPE SCREEN ==========================
# =====================================================================

def show_final_escape(prev_frame):
    prev_frame.Close()

    global total_mistakes
    frame = wx.Frame(None, title="🏆 ESCAPED!", size=(600, 320))
    panel = wx.Panel(frame)
    panel.SetBackgroundColour(wx.Colour(5, 15, 30))

    total_time = time.time() - game_start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)

    title = wx.StaticText(panel, label="MISSION COMPLETE")
    title.SetForegroundColour(wx.Colour(0, 200, 255))
    title.SetFont(wx.Font(20, wx.FONTFAMILY_MODERN,
                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

    summary = wx.StaticText(panel,
        label=f"🎉 YOU ESCAPED ALL ROOMS!\n\n"
              f"⏱ Time: {minutes:02d}:{seconds:02d}\n"
              f"❌ Mistakes: {total_mistakes}\n\n"
              f"Good job Agent 🕵")
    summary.SetForegroundColour(wx.Colour(255, 255, 255))
    summary.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    summary.Wrap(540)
    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 25)
    vbox.Add(summary, 0, wx.ALIGN_CENTER | wx.ALL, 25)
    panel.SetSizer(vbox)
    frame.Show()

# =====================================================================
# ========================== ROOM 4 Q2 ================================
# =====================================================================

def room4_q2(prev_frame):
    prev_frame.Close()

    frame = wx.Frame(None, title="Room 4 – Gate Q2", size=(500, 330))
    panel = wx.Panel(frame)
    panel.SetBackgroundColour(wx.Colour(5, 5, 12))

    vbox = wx.BoxSizer(wx.VERTICAL)

    title = wx.StaticText(panel, label="ROOM 4 – ENCRYPTION GATE (Q2)")
    puzzle = wx.StaticText(panel, label=f"Decrypt (shift {shift_2}): {enc2}")
    hint = wx.StaticText(panel, label="Hint: SYMBOL Caesar Cipher")

    hacker_text(title, 14, "GREEN")
    hacker_text(puzzle, 12, "CYAN")
    hacker_text(hint, 10, "YELLOW")

    input_box = wx.TextCtrl(panel)
    hacker_text(input_box, 12, "CYAN")

    result = wx.StaticText(panel, label="")
    hacker_text(result, 12, "YELLOW")

    def check(event):
        ans = input_box.GetValue().strip().upper()
        if ans == correct_2:
            result.SetLabel("🟢 GATE OVERRIDE SUCCESSFUL!")
            wx.CallLater(1000, lambda: show_final_escape(frame))
        else:
            add_mistake()
            result.SetLabel("🔴 ACCESS DENIED")

    btn = wx.Button(panel, label="ENTER CODE")
    hacker_button(btn, "GREEN")
    btn.Bind(wx.EVT_BUTTON, check)

    vbox.Add(title, 0, wx.ALL, 15)
    vbox.Add(puzzle, 0, wx.ALL, 10)
    vbox.Add(hint, 0, wx.ALL, 10)
    vbox.Add(input_box, 0, wx.EXPAND | wx.ALL, 10)
    vbox.Add(btn, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
    vbox.Add(result, 0, wx.ALL, 10)

    panel.SetSizer(vbox)
    frame.Show()

# =====================================================================
# ========================== ROOM 4 Q1 ================================
# =====================================================================

def room4_q1(prev_frame):
    prev_frame.Close()

    frame = wx.Frame(None, title="Room 4 – Gate Q1", size=(500, 330))
    panel = wx.Panel(frame)
    panel.SetBackgroundColour(wx.Colour(5, 5, 12))

    vbox = wx.BoxSizer(wx.VERTICAL)

    title = wx.StaticText(panel, label="ROOM 4 – ENCRYPTION GATE (Q1)")
    puzzle = wx.StaticText(panel, label=f"Decrypt (shift {shift_1}): {enc1}")
    hint = wx.StaticText(panel, label="Hint: SYMBOL Caesar Cipher")

    hacker_text(title, 14, "GREEN")
    hacker_text(puzzle, 12, "CYAN")
    hacker_text(hint, 10, "YELLOW")

    input_box = wx.TextCtrl(panel)
    hacker_text(input_box, 12, "CYAN")

    result = wx.StaticText(panel, label="")
    hacker_text(result, 12, "YELLOW")

    def check(event):
        ans = input_box.GetValue().strip().upper()
        if ans == correct_1:
            result.SetLabel("🟢 FIRST LOCK BYPASSED!")
            wx.CallLater(800, lambda: room4_q2(frame))
        else:
            add_mistake()
            result.SetLabel("🔴 WRONG")

    btn = wx.Button(panel, label="ENTER CODE")
    hacker_button(btn, "GREEN")
    btn.Bind(wx.EVT_BUTTON, check)

    vbox.Add(title, 0, wx.ALL, 15)
    vbox.Add(puzzle, 0, wx.ALL, 10)
    vbox.Add(hint, 0, wx.ALL, 10)
    vbox.Add(input_box, 0, wx.EXPAND | wx.ALL, 10)
    vbox.Add(btn, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
    vbox.Add(result, 0, wx.ALL, 10)

    panel.SetSizer(vbox)
    frame.Show()
    
# =====================================================================
# ========================== ROOM 3 Q2 ================================
# =====================================================================

hex_q1 = "2C"
hex_q2 = "7A9"
bits_q1 = 8
bits_q2 = 12
full1 = hex_to_full_binary(hex_q1, bits_q1)
full2 = hex_to_full_binary(hex_q2, bits_q2)
strip1 = full1.lstrip("0")
strip2 = full2.lstrip("0")

def room3_q2(prev_frame):
    prev_frame.Close()

    frame = wx.Frame(None, title="Room 3 – HEX Q2", size=(500, 330))
    panel = wx.Panel(frame)
    panel.SetBackgroundColour(wx.Colour(5, 5, 12))

    vbox = wx.BoxSizer(wx.VERTICAL)

    title = wx.StaticText(panel, label="ROOM 3 – HEX → BINARY (12 bits)")
    puzzle = wx.StaticText(panel, label=f"HEX: {hex_q2}")
    hint = wx.StaticText(panel, label="Hint: Convert HEX to binary (12 bits or stripped)")

    hacker_text(title, 14, "CYAN")
    hacker_text(puzzle, 12, "MAGENTA")
    hacker_text(hint, 10, "YELLOW")

    input_box = wx.TextCtrl(panel)
    hacker_text(input_box, 12, "CYAN")

    result = wx.StaticText(panel, label="")
    hacker_text(result, 12, "YELLOW")

    def check(event):
        ans = input_box.GetValue().strip().replace(" ", "")
        if ans == full2 or ans.lstrip("0") == strip2:
            result.SetLabel("✔ ACCESS GRANTED – ROOM 4...")
            wx.CallLater(1000, lambda: room4_q1(frame))
        else:
            add_mistake()
            result.SetLabel("❌ INVALID")

    btn = wx.Button(panel, label="ENTER")
    hacker_button(btn, "MAGENTA")
    btn.Bind(wx.EVT_BUTTON, check)

    vbox.Add(title, 0, wx.ALL, 15)
    vbox.Add(puzzle, 0, wx.ALL, 10)
    vbox.Add(hint, 0, wx.ALL, 10)
    vbox.Add(input_box, 0, wx.EXPAND | wx.ALL, 10)
    vbox.Add(btn, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
    vbox.Add(result, 0, wx.ALL, 10)

    panel.SetSizer(vbox)
    frame.Show()

# =====================================================================
# ========================== ROOM 3 Q1 ================================
# =====================================================================

def room3_q1(prev_frame):
    prev_frame.Close()

    frame = wx.Frame(None, title="Room 3 – HEX Q1", size=(500, 330))
    panel = wx.Panel(frame)
    panel.SetBackgroundColour(wx.Colour(5, 5, 12))

    vbox = wx.BoxSizer(wx.VERTICAL)

    title = wx.StaticText(panel, label="ROOM 3 – HEX → BINARY (8 bits)")
    puzzle = wx.StaticText(panel, label=f"HEX: {hex_q1}")
    hint = wx.StaticText(panel, label="Hint: Convert HEX to binary (8 bits or stripped)")

    hacker_text(title, 14, "CYAN")
    hacker_text(puzzle, 12, "MAGENTA")
    hacker_text(hint, 10, "YELLOW")

    input_box = wx.TextCtrl(panel)
    hacker_text(input_box, 12, "CYAN")

    result = wx.StaticText(panel, label="")
    hacker_text(result, 12, "YELLOW")

    def check(event):
        ans = input_box.GetValue().strip().replace(" ", "")
        if ans == full1 or ans.lstrip("0") == strip1:
            result.SetLabel("✔ ACCESS GRANTED")
            wx.CallLater(800, lambda: room3_q2(frame))
        else:
            add_mistake()
            result.SetLabel("❌ INVALID")

    btn = wx.Button(panel, label="ENTER")
    hacker_button(btn, "MAGENTA")
    btn.Bind(wx.EVT_BUTTON, check)

    vbox.Add(title, 0, wx.ALL, 15)
    vbox.Add(puzzle, 0, wx.ALL, 10)
    vbox.Add(hint, 0, wx.ALL, 10)
    vbox.Add(input_box, 0, wx.EXPAND | wx.ALL, 10)
    vbox.Add(btn, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
    vbox.Add(result, 0, wx.ALL, 10)

    panel.SetSizer(vbox)
    frame.Show()

# =====================================================================
# ========================= ROOM 2 – HACKER LAB =======================
# =====================================================================

STAGE1_SHIFT = 5
STAGE1_CIPHER = "ZSJIW"
STAGE1_ANSWER = "UNDER"

STAGE2_SHIFT = 21
STAGE2_PLAIN = "MASTER"
STAGE2_CIPHER = caesar_cipher(STAGE2_PLAIN, STAGE2_SHIFT, mode="encrypt")

def room2(prev_frame):
    prev_frame.Close()

    frame = wx.Frame(None, title="⚡ Room 2 – Hacker Lab ⚡", size=(600, 400))
    panel = wx.Panel(frame)
    panel.SetBackgroundColour(wx.Colour(3, 8, 15))

    vbox = wx.BoxSizer(wx.VERTICAL)

    stage = {"value": 1}

    puzzle = wx.StaticText(panel,
        label=f"💠 STAGE 1 – Solve x² - x - 20 = 0\n\nEncrypted: {STAGE1_CIPHER}"
    )
    hacker_text(puzzle, 14, "CYAN")
    puzzle.Wrap(460)

    input_box = wx.TextCtrl(panel)
    hacker_text(input_box, 13, "GREEN")

    result = wx.StaticText(panel, label="")
    hacker_text(result, 12, "YELLOW")

    def check(event):
        ans = input_box.GetValue().strip().upper()

        if stage["value"] == 1:
            if ans == STAGE1_ANSWER:
                result.SetLabel("🟢 Stage 1 Complete!")
                stage["value"] = 2
                input_box.SetValue("")
                puzzle.SetLabel(
                    f"💠 STAGE 2 – Modular Prime Cipher\n\n"
                    f"Encrypted: {STAGE2_CIPHER}\nShift = (17+4) mod 26"
                )
                puzzle.Wrap(460)
            else:
                add_mistake()
                result.SetLabel("🔴 Wrong")

        else:
            if ans == STAGE2_PLAIN:
                result.SetLabel("🟢 Hacker Terminal Unlocked!")
                wx.CallLater(1000, lambda: room3_q1(frame))
            else:
                add_mistake()
                result.SetLabel("🔴 Wrong")

    btn = wx.Button(panel, label="EXECUTE")
    hacker_button(btn, "MAGENTA")
    btn.Bind(wx.EVT_BUTTON, check)

    vbox.Add(puzzle, 0, wx.ALL | wx.ALIGN_CENTER, 15)
    vbox.Add(input_box, 0, wx.EXPAND | wx.ALL, 10)
    vbox.Add(btn, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
    vbox.Add(result, 0, wx.ALL | wx.ALIGN_CENTER, 10)

    panel.SetSizer(vbox)
    frame.Show()

# =====================================================================
# ============================== ROOM 1 ================================
# =====================================================================

def room1(prev_frame):
    if prev_frame:
        prev_frame.Close()

    frame = wx.Frame(None, title="🔐 Escape Room – Room 1", size=(700, 450))
    panel = wx.Panel(frame)
    panel.SetBackgroundColour("#1e1e1e")

    vbox = wx.BoxSizer(wx.VERTICAL)

    stage = {"value": 1}

    title = wx.StaticText(panel, label="🔒 Welcome to the Escape Room 🔒")
    title.SetFont(wx.Font(18, wx.FONTFAMILY_MODERN,
                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    title.SetForegroundColour("#ffa500")

    puzzle = wx.StaticText(panel, label="")
    puzzle.SetFont(wx.Font(14, wx.FONTFAMILY_TELETYPE,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    puzzle.SetForegroundColour("#ffffff")

    result = wx.StaticText(panel, label="")
    result.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    result.SetForegroundColour("#00ff99")

    input_box = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
    input_box.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                              wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

    submit = wx.Button(panel, label="Submit Answer")

    def load():
        result.SetLabel("")
        input_box.SetValue("")
        s = stage["value"]

        if s == 1:
            puzzle.SetLabel("Puzzle 1:\nEncrypted: KHOOR (Shift 3)")
            answer = "HELLO"
        elif s == 2:
            puzzle.SetLabel("Puzzle 2:\nEncrypted: GSV XLWV RH ZOO (Atbash-each letter in the encrypted message is replaced by its corresponding letter from the opposite end of the alphabet)")
            answer = "THE CODE IS ALL"
        elif s == 3:
            puzzle.SetLabel("Puzzle 3:\nEncrypted: URYYB JBEYQ (ROT13-shift 13)")
            answer = "HELLO WORLD"
        else:
            puzzle.SetLabel("🎉 ROOM 1 COMPLETE!")
            input_box.Hide()
            submit.Hide()
            wx.CallLater(1200, lambda: room2(frame))
            return

        stage["answer"] = answer

    def check(event):
        ans = input_box.GetValue().strip().upper()
        if ans == stage["answer"]:
            result.SetLabel("✔ Correct!")
            stage["value"] += 1
            wx.CallLater(1000, load)
        else:
            add_mistake()
            result.SetLabel("❌ Wrong")

    submit.Bind(wx.EVT_BUTTON, check)
    input_box.Bind(wx.EVT_TEXT_ENTER, check)

    vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 20)
    vbox.Add(puzzle, 0, wx.ALIGN_CENTER | wx.TOP, 30)
    vbox.Add(input_box, 0, wx.ALIGN_CENTER | wx.TOP, 20)
    vbox.Add(submit, 0, wx.ALIGN_CENTER | wx.TOP, 10)
    vbox.Add(result, 0, wx.ALIGN_CENTER | wx.TOP, 20)

    panel.SetSizer(vbox)

    load()
    frame.Show()

# =====================================================================
# =============================== MAIN ================================
# =====================================================================

if __name__ == "__main__":
    app = wx.App()
    start_menu()
    app.MainLoop()
