import tkinter as tk
from tkinter import ttk, messagebox
import random

try:
    from deep_translator import MyMemoryTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

# Available Target Languages
LANGUAGES = {
    'Spanish': 'es-ES',
    'French': 'fr-FR',
    'German': 'de-DE',
    'Italian': 'it-IT',
    'Japanese': 'ja-JP',
    'Chinese': 'zh-CN',
    'Russian': 'ru-RU',
    'Hindi': 'hi-IN',
    'Portuguese': 'pt-PT',
    'Dutch': 'nl-NL',
    'Arabic': 'ar-SA',
    'Korean': 'ko-KR',
    'Turkish': 'tr-TR',
    'Polish': 'pl-PL'
}

class TranslationBattleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("TRANSLATION SPELLCASTER // BOSS BATTLE")
        self.root.geometry("650x720")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        # Game Stats
        self.boss_hp = 500
        self.max_boss_hp = 500
        self.score = 0
        self.used_languages = set()

        # UI Styling Colors
        self.BG_DARK = "#0f172a"
        self.PANEL_BG = "#1e293b"
        self.TEXT_COLOR = "#f8fafc"
        self.CYAN = "#38bdf8"
        self.AMBER = "#fbbf24"
        self.RED = "#f43f5e"
        self.GREEN = "#4ade80"

        self.build_ui()

    def build_ui(self):
        # Header / Boss Area
        boss_frame = tk.Frame(self.root, bg=self.PANEL_BG, bd=2, relief="groove")
        boss_frame.pack(fill="x", padx=20, pady=15)

        tk.Label(boss_frame, text="👾 LANGUAGE GOLEM (BOSS)", font=("Arial", 16, "bold"), fg=self.RED, bg=self.PANEL_BG).pack(pady=(10, 5))

        # Health Bar
        self.hp_label = tk.Label(boss_frame, text=f"HP: {self.boss_hp} / {self.max_boss_hp}", font=("Arial", 11, "bold"), fg=self.AMBER, bg=self.PANEL_BG)
        self.hp_label.pack()

        self.hp_bar = ttk.Progressbar(boss_frame, length=500, mode='determinate')
        self.hp_bar['value'] = 100
        self.hp_bar.pack(pady=(5, 15))

        # Stats Counter
        stats_frame = tk.Frame(self.root, bg=self.BG_DARK)
        stats_frame.pack(fill="x", padx=25, pady=5)

        self.score_lbl = tk.Label(stats_frame, text="SCORE: 0", font=("Arial", 12, "bold"), fg=self.AMBER, bg=self.BG_DARK)
        self.score_lbl.pack(side="left")

        self.lang_count_lbl = tk.Label(stats_frame, text="LANGUAGES DISCOVERED: 0", font=("Arial", 11, "bold"), fg=self.CYAN, bg=self.BG_DARK)
        self.lang_count_lbl.pack(side="right")

        # Player Input Section
        input_panel = tk.Frame(self.root, bg=self.PANEL_BG, bd=2, relief="groove")
        input_panel.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(input_panel, text="1. TYPE ANY WORD OR PHRASE:", font=("Arial", 11, "bold"), fg=self.TEXT_COLOR, bg=self.PANEL_BG).pack(anchor="w", padx=15, pady=(15, 5))

        self.user_input = tk.Entry(input_panel, font=("Arial", 14), bg="#0f172a", fg=self.GREEN, insertbackground=self.GREEN, justify="center")
        self.user_input.pack(fill="x", padx=15, pady=5, ipady=6)
        self.user_input.bind("<Return>", lambda e: self.cast_spell())

        tk.Label(input_panel, text="2. CHOOSE TARGET LANGUAGE:", font=("Arial", 11, "bold"), fg=self.TEXT_COLOR, bg=self.PANEL_BG).pack(anchor="w", padx=15, pady=(10, 5))

        self.lang_combobox = ttk.Combobox(input_panel, values=list(LANGUAGES.keys()), state="readonly", font=("Arial", 11))
        self.lang_combobox.set("Spanish")
        self.lang_combobox.pack(fill="x", padx=15, pady=5)

        # Attack Button
        attack_btn = tk.Button(input_panel, text="⚡ CAST TRANSLATION ATTACK ⚡", font=("Arial", 12, "bold"), bg=self.CYAN, fg="#0f172a", activebackground=self.GREEN, command=self.cast_spell)
        attack_btn.pack(pady=15, ipady=5, padx=15, fill="x")

        # Spell Result Display
        self.result_lbl = tk.Label(input_panel, text="Type a word and select a language to attack!", font=("Arial", 12, "bold"), fg=self.AMBER, bg=self.PANEL_BG, wraplength=550)
        self.result_lbl.pack(pady=(5, 15))

    def cast_spell(self):
        if self.boss_hp <= 0:
            messagebox.showinfo("Victory!", "The boss is defeated! Restarting battle...")
            self.reset_boss()
            return

        text_to_translate = self.user_input.get().strip()
        selected_language = self.lang_combobox.get()
        target_code = LANGUAGES[selected_language]

        if not text_to_translate:
            self.result_lbl.config(text="⚠️ Please type a word or phrase first!", fg=self.AMBER)
            return

        # Perform translation
        try:
            translator = MyMemoryTranslator(source='en-US', target=target_code)
            translated_text = translator.translate(text_to_translate)
        except Exception as e:
            self.result_lbl.config(text="❌ Translation server error. Try another word or language.", fg=self.RED)
            return

        # Calculate Attack Power / Damage based on translated length & bonuses
        base_damage = len(translated_text) * 12
        variety_bonus = 50 if selected_language not in self.used_languages else 0
        total_damage = base_damage + variety_bonus

        self.used_languages.add(selected_language)
        self.boss_hp = max(0, self.boss_hp - total_damage)
        self.score += total_damage

        # Update Health Bar
        hp_percentage = (self.boss_hp / self.max_boss_hp) * 100
        self.hp_bar['value'] = hp_percentage
        self.hp_label.config(text=f"HP: {self.boss_hp} / {self.max_boss_hp}")
        self.score_lbl.config(text=f"SCORE: {self.score}")
        self.lang_count_lbl.config(text=f"LANGUAGES DISCOVERED: {len(self.used_languages)}")

        # Clear Input Box
        self.user_input.delete(0, tk.END)

        # Combat Display Message
        bonus_msg = f" (+50 New Language Bonus!)" if variety_bonus > 0 else ""
        self.result_lbl.config(
            text=f"✨ TRANSLATED: '{translated_text}' ({selected_language})\n💥 DEALT {total_damage} DAMAGE!{bonus_msg}",
            fg=self.GREEN
        )

        if self.boss_hp <= 0:
            self.result_lbl.config(text=f"🏆 BOSS DEFEATED! Final Score: {self.score}", fg=self.AMBER)

    def reset_boss(self):
        self.max_boss_hp += 250
        self.boss_hp = self.max_boss_hp
        self.hp_bar['value'] = 100
        self.hp_label.config(text=f"HP: {self.boss_hp} / {self.max_boss_hp}")
        self.result_lbl.config(text="A stronger Golem appears! Keep translating to attack!", fg=self.CYAN)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationBattleGame(root)
    root.mainloop()
