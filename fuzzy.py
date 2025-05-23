import sys
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QSlider, QSizePolicy, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Bulanık değişkenler
protein = ctrl.Antecedent(np.arange(0, 301, 1), 'protein')
carb = ctrl.Antecedent(np.arange(0, 301, 1), 'carb')
fat = ctrl.Antecedent(np.arange(0, 301, 1), 'fat')
sugar = ctrl.Antecedent(np.arange(0, 101, 1), 'sugar')
stress = ctrl.Antecedent(np.arange(1, 6, 1), 'stress')

muscle_gain = ctrl.Consequent(np.arange(0, 11, 1), 'muscle_gain')
fat_loss = ctrl.Consequent(np.arange(0, 11, 1), 'fat_loss')

# Üyelik fonksiyonları
protein['low'] = fuzz.trimf(protein.universe, [0, 0, 100])
protein['medium'] = fuzz.trimf(protein.universe, [50, 150, 250])
protein['high'] = fuzz.trimf(protein.universe, [200, 300, 300])

carb['low'] = fuzz.trimf(carb.universe, [0, 0, 100])
carb['medium'] = fuzz.trimf(carb.universe, [50, 150, 250])
carb['high'] = fuzz.trimf(carb.universe, [200, 300, 300])

fat['low'] = fuzz.trimf(fat.universe, [0, 0, 100])
fat['medium'] = fuzz.trimf(fat.universe, [50, 150, 250])
fat['high'] = fuzz.trimf(fat.universe, [200, 300, 300])

sugar['low'] = fuzz.trimf(sugar.universe, [0, 0, 30])
sugar['medium'] = fuzz.trimf(sugar.universe, [20, 50, 80])
sugar['high'] = fuzz.trimf(sugar.universe, [60, 100, 100])

stress['low'] = fuzz.trimf(stress.universe, [1, 1, 2])
stress['medium'] = fuzz.trimf(stress.universe, [2, 3, 4])
stress['high'] = fuzz.trimf(stress.universe, [3, 5, 5])

muscle_gain['very_low'] = fuzz.trimf(muscle_gain.universe, [0, 0, 2])
muscle_gain['low'] = fuzz.trimf(muscle_gain.universe, [1, 3, 5])
muscle_gain['medium'] = fuzz.trimf(muscle_gain.universe, [4, 5.5, 7])
muscle_gain['high'] = fuzz.trimf(muscle_gain.universe, [6, 8, 9])
muscle_gain['very_high'] = fuzz.trimf(muscle_gain.universe, [8, 10, 10])

fat_loss['very_low'] = fuzz.trimf(fat_loss.universe, [0, 0, 2])
fat_loss['low'] = fuzz.trimf(fat_loss.universe, [1, 3, 5])
fat_loss['medium'] = fuzz.trimf(fat_loss.universe, [4, 5.5, 7])
fat_loss['high'] = fuzz.trimf(fat_loss.universe, [6, 8, 9])
fat_loss['very_high'] = fuzz.trimf(fat_loss.universe, [8, 10, 10])

rules = [
    ctrl.Rule(protein['high'] & carb['high'] & fat['low'] & sugar['low'] & stress['low'], muscle_gain['very_high']),
    ctrl.Rule(protein['high'] & carb['medium'] & fat['low'] & sugar['low'] & stress['low'], muscle_gain['high']),
    ctrl.Rule(protein['high'] & carb['medium'] & fat['medium'] & sugar['medium'] & stress['medium'], muscle_gain['medium']),
    ctrl.Rule(protein['medium'] & carb['medium'] & fat['low'] & sugar['low'] & stress['medium'], muscle_gain['medium']),
    ctrl.Rule(protein['medium'] & carb['low'] & (fat['medium'] | sugar['medium']) & stress['high'], muscle_gain['low']),
    ctrl.Rule(protein['low'] & stress['medium'], muscle_gain['low']),
    ctrl.Rule(protein['low'] & stress['high'], muscle_gain['very_low']),
    ctrl.Rule(protein['low'] & fat['high'] & sugar['high'] & stress['high'], muscle_gain['very_low']),
    ctrl.Rule(protein['medium'] & fat['high'] & sugar['high'], muscle_gain['very_low']),
    ctrl.Rule(protein['medium'] & stress['high'] & (fat['medium'] | sugar['medium']), muscle_gain['low']),
    ctrl.Rule(protein['high'] & carb['low'], muscle_gain['medium']),
    ctrl.Rule(protein['medium'] & carb['low'], muscle_gain['low']),
    ctrl.Rule(protein['low'] & carb['high'], muscle_gain['low']),
    ctrl.Rule(fat['low'] & sugar['low'] & stress['high'] & carb['low'], fat_loss['very_high']),
    ctrl.Rule(fat['low'] & sugar['low'] & stress['medium'] & carb['medium'], fat_loss['high']),
    ctrl.Rule(fat['low'] & sugar['medium'] & stress['high'], fat_loss['high']),
    ctrl.Rule(fat['medium'] & sugar['low'] & stress['high'], fat_loss['medium']),
    ctrl.Rule(fat['medium'] & sugar['medium'] & stress['medium'], fat_loss['medium']),
    ctrl.Rule(fat['high'] & sugar['high'], fat_loss['very_low']),
    ctrl.Rule(fat['high'] & stress['low'], fat_loss['low']),
    ctrl.Rule(fat['medium'] & sugar['high'] & stress['low'], fat_loss['low']),
    ctrl.Rule(carb['high'] & fat['low'] & sugar['low'] & stress['high'], fat_loss['medium']),
    ctrl.Rule(carb['low'] & fat['low'] & sugar['low'] & stress['high'], fat_loss['very_high']),
    ctrl.Rule(carb['low'] & fat['medium'] & stress['medium'], fat_loss['high']),
    ctrl.Rule(carb['low'] & fat['high'], fat_loss['low']),
]

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

class FuzzyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bulanık Kontrolcü - Kas Kazanımı ve Yağ Yakımı")
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 14px;
                background-color: #f0f4f7;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 6px;
                background-color: #2d89ef;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1b5fad;
            }
            QLabel {
                margin: 3px;
            }
        """)
        self.input_canvases = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.main_tab_layout = QVBoxLayout(self.main_tab)

        self.inputs = {}
        for label_text, minv, maxv in [
            ("Protein (0-300 g)", 0, 300),
            ("Karbonhidrat (0-300 g)", 0, 300),
            ("Yağ (0-300 g)", 0, 300),
            ("Şeker (0-100 g)", 0, 100),
        ]:
            h = QHBoxLayout()
            label = QLabel(label_text)
            inp = QLineEdit()
            inp.setPlaceholderText(f"{minv} - {maxv}")
            h.addWidget(label)
            h.addWidget(inp)
            self.inputs[label_text] = inp
            self.main_tab_layout.addLayout(h)

        h_stress = QHBoxLayout()
        label_stress = QLabel("Antrenman Stresi (1-5)")
        self.stress_slider = QSlider(Qt.Horizontal)
        self.stress_slider.setMinimum(1)
        self.stress_slider.setMaximum(5)
        self.stress_slider.setTickInterval(1)
        self.stress_slider.setTickPosition(QSlider.TicksBelow)
        self.stress_value_label = QLabel("1")
        self.stress_slider.valueChanged.connect(lambda: self.stress_value_label.setText(str(self.stress_slider.value())))
        h_stress.addWidget(label_stress)
        h_stress.addWidget(self.stress_slider)
        h_stress.addWidget(self.stress_value_label)
        self.main_tab_layout.addLayout(h_stress)

        self.calc_btn = QPushButton("Hesapla")
        self.calc_btn.clicked.connect(self.calculate)
        self.main_tab_layout.addWidget(self.calc_btn)

        self.muscle_label = QLabel("Kas Kazanımı: -")
        self.fat_label = QLabel("Yağ Yakımı: -")
        self.main_tab_layout.addWidget(self.muscle_label)
        self.main_tab_layout.addWidget(self.fat_label)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.main_tab_layout.addWidget(self.canvas)

        for var in [protein, carb, fat, sugar, stress]:
            tab = QWidget()
            vbox = QVBoxLayout(tab)
            fig = Figure(figsize=(5, 3))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            for label in var.terms:
                ax.plot(var.universe, var[label].mf, label=label)
            ax.set_title(f"{var.label.capitalize()} Üyelik Fonksiyonları")
            ax.legend()
            vbox.addWidget(canvas)
            self.tabs.addTab(tab, var.label.capitalize())
            self.input_canvases[var.label] = (canvas, ax)

        self.tabs.addTab(self.main_tab, "Hesaplama")
        self.tabs.setCurrentWidget(self.main_tab)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def calculate(self):
        try:
            p = float(self.inputs["Protein (0-300 g)"].text())
            c = float(self.inputs["Karbonhidrat (0-300 g)"].text())
            f = float(self.inputs["Yağ (0-300 g)"].text())
            s = float(self.inputs["Şeker (0-100 g)"].text())
            st = self.stress_slider.value()

            sim.input['protein'] = p
            sim.input['carb'] = c
            sim.input['fat'] = f
            sim.input['sugar'] = s
            sim.input['stress'] = st
            sim.compute()

            mg = sim.output['muscle_gain']
            fl = sim.output['fat_loss']

            self.muscle_label.setText(f"Kas Kazanımı: {mg:.2f} / 10")
            self.fat_label.setText(f"Yağ Yakımı: {fl:.2f} / 10")
            self.plot_results(mg, fl)

            self.update_input_graphs({
                'protein': p,
                'carb': c,
                'fat': f,
                'sugar': s,
                'stress': st
            })

        except:
            self.muscle_label.setText("Hata: Kurallara aykırı giriş.")
            self.fat_label.setText("")

    def plot_results(self, mg, fl):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        categories = ['Kas Kazanımı', 'Yağ Yakımı']
        values = [mg, fl]
        bars = ax.bar(categories, values, color=['#4caf50', '#f44336'])
        ax.set_ylim(0, 10)
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{yval:.2f}", ha='center')
        self.canvas.draw()

    def update_input_graphs(self, inputs):
        for key, value in inputs.items():
            if key in self.input_canvases:
                canvas, ax = self.input_canvases[key]
                ax.clear()
                var = eval(key)
                for label in var.terms:
                    ax.plot(var.universe, var[label].mf, label=label)
                ax.axvline(value, color='red', linestyle='--', label=f"Giriş: {value}")
                ax.set_title(f"{key.capitalize()} Üyelik Fonksiyonları")
                ax.legend()
                canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FuzzyApp()
    window.show()
    sys.exit(app.exec())
