import lal
import lalsimulation as lalsim


def compute_antenna_ratio(freq, ra, dec, psi):
    # Get detector structures
    h1_det = lalsim.DetectorPrefixToLALDetector('H1')
    l1_det = lalsim.DetectorPrefixToLALDetector('L1')

    t = 1126259462  # GPS time for GW150914
    gmst = lal.GreenwichMeanSiderealTime(t)

    # Compute antenna response
    f_plus_H1, f_cross_H1 = lal.ComputeDetAMResponse(h1_det.response, ra, dec, psi, gmst)
    f_plus_L1, f_cross_L1 = lal.ComputeDetAMResponse(l1_det.response, ra, dec, psi, gmst)

    # Combine responses as RMS average
    resp_H1 = (f_plus_H1**2 + f_cross_H1**2)**0.5
    resp_L1 = (f_plus_L1**2 + f_cross_L1**2)**0.5
    return resp_H1 / resp_L1 if resp_L1 != 0 else float('inf')
