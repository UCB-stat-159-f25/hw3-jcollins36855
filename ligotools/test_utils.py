import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import os
from ligotools.utils import whiten, matched_filter_analysis

def test_whiten():
    """
    Small functional test for whiten().
    Ensures output has same length and no NaNs.
    """
    # --- synthetic data ---
    fs = 1024
    dt = 1/fs
    t = np.linspace(0, 1, fs)
    strain = np.sin(2*np.pi*50*t) + 0.1*np.random.randn(len(t))

    # constant PSD
    freqs = np.fft.rfftfreq(len(t), dt)
    psd = np.ones_like(freqs) * 2e-22
    interp_psd = interp1d(freqs, psd, bounds_error=False, fill_value="extrapolate")

    # run
    white_ht = whiten(strain, interp_psd, dt)

    # --- basic checks ---
    assert len(white_ht) == len(strain), "Output length mismatch"
    assert not np.isnan(white_ht).any(), "NaNs found in whitened output"

    print("✅ test_whiten passed successfully.")



def test_matched_filter_analysis():
    """
    Lightweight test of matched_filter_analysis() using synthetic data.
    Confirms outputs exist, shapes match, and results look reasonable.
    """
    # --- synthetic setup ---
    fs = 1024
    dt = 1/fs
    t = np.linspace(0, 2, 2*fs)
    template_p = np.sin(2*np.pi*50*t)
    template_c = np.cos(2*np.pi*50*t)
    template_offset = 0
    tevent = 1.0
    eventname = "test_event"

    # Fake data for detectors (template + small noise)
    strain_H1 = template_p + 0.1*np.random.randn(len(t))
    strain_L1 = template_p + 0.1*np.random.randn(len(t))
    strain_H1_whitenbp = strain_H1
    strain_L1_whitenbp = strain_L1

    # Simple bandpass filter
    bb, ab = butter(4, [20/(fs/2), 300/(fs/2)], btype='band')
    normalization = 1.0

    # --- call the function ---
    results, template_L1, template_H1 = matched_filter_analysis(
        strain_H1, strain_L1, t, template_p, template_c,
        template_offset, fs, tevent, eventname,
        strain_H1_whitenbp, strain_L1_whitenbp,
        bb, ab, normalization, whiten, filtfilt, dt,
        make_plots=False
    )

    # --- assertions ---
    assert isinstance(results, dict), "Results should be a dict"
    assert 'H1' in results and 'L1' in results, "Missing detector keys"
    assert np.isfinite(results['H1']['SNRmax']), "H1 SNRmax is not finite"
    assert np.isfinite(results['L1']['SNRmax']), "L1 SNRmax is not finite"
    assert template_L1.shape == template_H1.shape, "Template shapes mismatch"
    assert len(template_L1) == len(t), "Template length mismatch"

    print("✅ test_matched_filter_analysis passed successfully.")