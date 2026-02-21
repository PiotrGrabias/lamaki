import numpy as np
import matplotlib.pyplot as plt

# Dane z tabeli
thresholds = np.array([
    0.0250, 0.0500, 0.0750, 0.1000, 0.1250, 0.1500, 0.1750, 0.2000, 0.2250, 0.2500,
    0.2750, 0.3000, 0.3250, 0.3500, 0.3750, 0.4000, 0.4250, 0.4500, 0.4750, 0.5000,
    0.5250, 0.5500, 0.5750, 0.6000, 0.6250, 0.6500, 0.6750, 0.7000, 0.7250, 0.7500,
    0.7750, 0.8000, 0.8250, 0.8500, 0.8750, 0.9000, 0.9250, 0.9500, 0.9750, 1.0000
])

TP = np.array([
    100, 99, 98, 98, 97, 96, 96, 96, 94, 94,
    94, 94, 94, 94, 94, 94, 93, 93, 93, 93,
    93, 93, 93, 93, 93, 93, 93, 92, 92, 92,
    91, 91, 89, 80, 69, 54, 40, 21, 8, 0
])

FP = np.array([
    0, 1, 2, 2, 3, 4, 4, 4, 6, 6,
    6, 6, 6, 6, 6, 6, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
    9, 9, 11, 20, 31, 46, 60, 79, 92, 100
])

TN = np.array([
    0, 0, 0, 0, 1, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 3, 7, 7, 35, 47, 49,
    51, 58, 67, 77, 87, 95, 98, 98, 100, 100
])

FN = np.array([
    100, 100, 100, 100, 99, 98, 98, 98, 98, 98,
    98, 98, 98, 98, 98, 98, 98, 98, 98, 98,
    98, 98, 98, 98, 97, 93, 93, 65, 53, 51,
    49, 42, 33, 23, 13, 5, 2, 2, 0, 0
])

# Obliczenia wskaźników
TPR = np.zeros_like(TP, dtype=float)
FPR = np.zeros_like(FP, dtype=float)

pos_sum = TP + FN
neg_sum = FP + TN

TPR[pos_sum != 0] = TP[pos_sum != 0] / pos_sum[pos_sum != 0]
FPR[neg_sum != 0] = FP[neg_sum != 0] / neg_sum[neg_sum != 0]

FNMR = 1 - TPR  # False Non-Match Rate
FMR = FPR       # False Match Rate

# Obliczenie AUC
idx_sort = np.argsort(FPR)
FPR_sorted = FPR[idx_sort]
TPR_sorted = TPR[idx_sort]
AUC = np.trapezoid(TPR_sorted, FPR_sorted)

# Obliczenie EER - punkt, gdzie FMR i FNMR są najbliższe
diff = np.abs(FMR - FNMR)
eer_index = np.argmin(diff)
eer = (FMR[eer_index] + FNMR[eer_index]) / 2
eer_threshold = thresholds[eer_index]

# Wykres ROC
plt.figure(figsize=(8,6))
plt.plot(FPR, TPR, marker='o', label='Krzywa ROC')
plt.plot([0,1], [0,1], 'k--', label='Losowy klasyfikator')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('Krzywa ROC')
plt.grid(True)
plt.legend()

# Wykres FMR i FNMR z zaznaczonym EER
plt.figure(figsize=(8,6))
plt.plot(thresholds, FMR, label='FMR (False Match Rate)')
plt.plot(thresholds, FNMR, label='FNMR (False Non-Match Rate)')
plt.axvline(eer_threshold, color='red', linestyle='--', label=f'EER ≈ {eer:.3f} przy progu {eer_threshold:.3f}')
plt.xlabel('Próg decyzyjny')
plt.ylabel('Wartość')
plt.title('FMR i FNMR oraz punkt EER')
plt.legend()
plt.grid(True)

plt.show()

print(f"AUC: {AUC:.4f}")
print(f"EER: {eer:.4f} przy progu {eer_threshold:.4f}")