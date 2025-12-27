# QCAL Privacy Policy

**Effective Date**: 2025-01-15  
**Version**: 1.0

---

## Our Commitment

QCAL (Quantum Coherence Analysis for LLMs) is committed to protecting your privacy and ensuring transparency in how we handle data. This policy reflects our core principles:

1. **No telemetry by default**: QCAL does not collect or transmit any usage data unless you explicitly opt in.
2. **Your data stays yours**: Analysis data never leaves your system without your permission.
3. **Open source transparency**: Our code is open for inspection, so you can verify our privacy claims.
4. **Informed consent**: Any data collection requires explicit opt-in with clear explanation.

---

## What Data QCAL Does NOT Collect

By default, QCAL does **NOT** collect:

- ❌ Usage statistics (command frequency, runtime, errors)
- ❌ System information (OS, CPU, RAM, Python version)
- ❌ Analysis parameters (catalogs, detectors, frequencies)
- ❌ Analysis results (SNR, p-values, detected events)
- ❌ LIGO/Virgo data you download
- ❌ Custom configuration files
- ❌ API keys or credentials
- ❌ Network activity logs
- ❌ Crash reports or stack traces
- ❌ Personal information of any kind

**Verification**: Check the source code at [https://github.com/motanova84/141hz](https://github.com/motanova84/141hz). Search for telemetry or analytics - you won't find it.

---

## Optional Telemetry (Opt-In Only)

Starting with **QCAL v0.2**, we may offer **optional** telemetry to help improve the software. This will always be:

- ✅ **Opt-in**: Disabled by default, requires explicit consent
- ✅ **Transparent**: Exact data collected is documented
- ✅ **Revocable**: Can be disabled at any time
- ✅ **Anonymous**: No personally identifiable information
- ✅ **Open source**: Telemetry code is part of the open-source repository

### How to Opt In (Future Feature)

```bash
# Enable telemetry (not yet implemented)
qcal telemetry --enable

# View what data would be sent
qcal telemetry --show

# Disable telemetry
qcal telemetry --disable
```

### What Optional Telemetry Might Include

If you opt in, we may collect:

1. **Aggregate usage statistics**:
   - Number of analyses run per week (no details about events or results)
   - Command frequency (e.g., "analyze" used 50 times, "validate" used 10 times)
   - Error types (e.g., "FileNotFoundError" occurred 5 times - no file paths)

2. **Performance metrics**:
   - Analysis runtime (for performance optimization)
   - Memory usage (to identify bottlenecks)

3. **Configuration (anonymized)**:
   - Python version (e.g., "3.11.5")
   - OS type (e.g., "Linux", "macOS" - no version details)
   - QCAL version (e.g., "0.2.0")

**Never collected**, even with opt-in:
- Specific event names (GW150914, etc.)
- Analysis results (SNR values, frequencies)
- File paths or filenames
- IP addresses
- Personal information

### Data Retention

- **Telemetry data**: Retained for 12 months, then deleted
- **Aggregate reports**: Non-identifiable summaries may be retained indefinitely for research

---

## Data You Provide to Third Parties

### GWOSC (Gravitational Wave Open Science Center)

When you use QCAL to download data from GWOSC:

- **Connection**: QCAL connects to [https://gwosc.org](https://gwosc.org) on your behalf
- **Data sent**: Event name (e.g., "GW150914"), detector name (e.g., "H1")
- **GWOSC privacy policy**: [https://gwosc.org/about/](https://gwosc.org/about/)
- **QCAL involvement**: QCAL acts as a client; we do not receive or store your GWOSC requests

**Your control**: You can download data manually and use local files instead:

```bash
# Use local data (no network access)
qcal analyze --data-dir /path/to/local/data
```

### Optional: Error Reporting Services

If you choose to report a bug via GitHub Issues:

- **Data shared**: You choose what to include in the issue report
- **Recommendation**: Exclude sensitive paths, API keys, or personal information
- **GitHub's policy**: [https://docs.github.com/en/site-policy/privacy-policies](https://docs.github.com/en/site-policy/privacy-policies)

---

## Data Stored Locally

QCAL stores data on your system:

1. **Cache directory**: `~/.qcal/cache/`
   - Downloaded GWOSC data (HDF5 files)
   - Intermediate analysis results (for performance)

2. **Configuration file**: `~/.qcal/config.yaml`
   - Your preferences (e.g., default detector, precision)
   - API keys (if you provide them) - stored locally only

3. **Output directories**: User-specified (e.g., `artifacts/`)
   - Analysis results (JSON, CSV, PNG, PDF)
   - Logs and metadata

**Your control**:
- Clear cache anytime: `qcal cache --clear`
- Inspect stored data: `qcal cache --list`
- Choose custom output locations: `qcal analyze --outdir /your/path`

**Data security**:
- QCAL does not encrypt local data (relies on OS-level protection)
- If you store API keys in `config.yaml`, set appropriate file permissions: `chmod 600 ~/.qcal/config.yaml`

---

## Enterprise Deployments

For organizations using QCAL at scale:

### On-Premises Deployment
- **Network isolation**: QCAL can run fully offline (use `--no-download` flag)
- **Data sovereignty**: All data stays within your infrastructure
- **Audit logs**: Enable local logging for compliance (GDPR, HIPAA, etc.)

### Cloud Deployment (Future: QCAL SaaS v1.0+)
- **Data residency**: Choose your region (US, EU, etc.)
- **Encryption**: Data encrypted in transit (TLS 1.3) and at rest (AES-256)
- **Access control**: Role-based access control (RBAC)
- **DPA available**: Data Processing Agreement for GDPR compliance

---

## Children's Privacy

QCAL is not intended for use by children under 13. We do not knowingly collect data from children.

If you believe a child has used QCAL and provided personal information, please contact us to have it removed.

---

## International Users

QCAL is developed primarily in [Your Country] but is used worldwide.

- **GDPR (EU)**: QCAL complies with GDPR by not collecting personal data without consent
- **CCPA (California)**: No personal data sale; opt-in for any data collection
- **Data transfers**: If telemetry is enabled, data may be transmitted to [Your Country] - you will be informed before opt-in

**Your rights**:
- Right to access your data (minimal since we don't collect much)
- Right to deletion (disable telemetry, clear cache)
- Right to portability (export configuration: `qcal config --export`)

---

## Changes to This Policy

We may update this policy as QCAL evolves. Changes will be:

- **Announced**: In CHANGELOG.md and GitHub Releases
- **Versioned**: Policy version number incremented
- **Opt-in required**: Any new data collection requires explicit re-consent

**Notification**: For major changes (e.g., introducing new telemetry), we will:
1. Update this file with 30 days notice
2. Require explicit re-opt-in for telemetry users
3. Post announcement in GitHub Discussions

---

## Open Source Transparency

QCAL is open source (Apache 2.0 license). You can:

- ✅ **Inspect the code**: Verify that we honor this privacy policy
- ✅ **Audit network activity**: Use Wireshark or similar tools to confirm no unexpected data transmission
- ✅ **Fork and modify**: Remove any features you don't trust
- ✅ **Report concerns**: Open a GitHub Issue if you find privacy violations

**Security research**: If you discover a privacy or security vulnerability, please report it responsibly via [SECURITY.md](SECURITY.md).

---

## Contact

**Privacy questions or concerns**:
- GitHub Issues: [https://github.com/motanova84/141hz/issues](https://github.com/motanova84/141hz/issues)
- GitHub Discussions: [https://github.com/motanova84/141hz/discussions](https://github.com/motanova84/141hz/discussions)
- Email: [Via GitHub profile]

**For GDPR/legal inquiries**:
- Tag your issue with `privacy` or `gdpr`
- We will respond within 30 days

---

## Summary

| Question | Answer |
|----------|--------|
| Does QCAL collect data by default? | **No** |
| Can I enable telemetry? | **Yes, opt-in only** (future feature) |
| Where is my analysis data stored? | **On your local system** |
| Can I use QCAL offline? | **Yes, with local data** |
| Is my data encrypted? | **In transit (GWOSC downloads); at rest (OS-level)** |
| Who can access my data? | **Only you** (unless you share it) |
| Can I delete all QCAL data? | **Yes, anytime** |

---

**TL;DR**: QCAL respects your privacy. No telemetry by default. Your data stays on your machine. Open source = verifiable trust.

---

*Last updated: 2025-01-15*  
*Policy version: 1.0*
