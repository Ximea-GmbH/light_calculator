"""
Light Calculator Core Module

This module implements the 4-step calculation process from scene illumination 
to electron count in camera sensor pixels.
"""

# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J⋅Hz⁻¹
SPEED_OF_LIGHT = 299792458  # m/s
LUX_CONVERSION_FACTOR = 683  # lm/W at 555nm


def calculate_scene_luminance(scene_illuminance, scene_reflectance):
    """
    Step 1: Convert scene illumination to scene luminance
    
    Args:
        scene_illuminance (float): Light falling on the scene (lux)
        scene_reflectance (float): Reflectance ratio (0-1)
    
    Returns:
        float: Scene luminance (nits/cd⋅m⁻²)
    """
    import math
    return (scene_illuminance * scene_reflectance) / math.pi


def calculate_sensor_illuminance(scene_luminance, lens_transmittance, f_number):
    """
    Step 2: Calculate illuminance on sensor through the lens
    
    Args:
        scene_luminance (float): Scene luminance (nits)
        lens_transmittance (float): Lens efficiency (0-1)
        f_number (float): Lens f-number
    
    Returns:
        float: Sensor illuminance (lux)
    """
    import math
    return (scene_luminance * lens_transmittance * math.pi) / (4 * f_number**2)


def calculate_photon_count(sensor_illuminance, pixel_size_um, exposure_time_ms, wavelength_nm):
    """
    Step 3: Convert sensor illuminance to photon count per pixel
    
    Args:
        sensor_illuminance (float): Illuminance on sensor (lux)
        pixel_size_um (float): Pixel width (micrometers)
        exposure_time_ms (float): Exposure duration (milliseconds)
        wavelength_nm (float): Average wavelength (nanometers)
    
    Returns:
        tuple: (photon_count, intermediate_values_dict)
    """
    # Convert sensor illuminance to irradiance
    sensor_irradiance = sensor_illuminance / LUX_CONVERSION_FACTOR  # W/m²
    
    # Calculate pixel area (convert μm to m)
    pixel_size_m = pixel_size_um * 1e-6
    pixel_area = pixel_size_m**2  # m²
    
    # Calculate energy of single photon (convert nm to m)
    wavelength_m = wavelength_nm * 1e-9
    photon_energy = (PLANCK_CONSTANT * SPEED_OF_LIGHT) / wavelength_m  # J
    
    # Convert exposure time to seconds
    exposure_time_s = exposure_time_ms / 1000
    
    # Calculate total photons per pixel
    total_energy_per_pixel = sensor_irradiance * pixel_area * exposure_time_s  # J
    photon_count = total_energy_per_pixel / photon_energy
    
    # Return intermediate values for transparency
    intermediate = {
        'sensor_irradiance_w_per_m2': sensor_irradiance,
        'pixel_area_m2': pixel_area,
        'photon_energy_j': photon_energy,
        'exposure_time_s': exposure_time_s,
        'total_energy_per_pixel_j': total_energy_per_pixel
    }
    
    return photon_count, intermediate


def calculate_electrons(photon_count, quantum_efficiency):
    """
    Step 4: Convert photons to electrons using quantum efficiency
    
    Args:
        photon_count (float): Number of photons per pixel
        quantum_efficiency (float): Sensor efficiency (0-1)
    
    Returns:
        float: Number of electrons generated
    """
    return photon_count * quantum_efficiency


def calculate_noise_analysis(signal_electrons, exposure_time_ms, read_noise_electrons, dark_current_e_per_s):
    """
    Calculate comprehensive noise analysis for camera sensor
    
    Args:
        signal_electrons (float): Signal electrons from light
        exposure_time_ms (float): Exposure time in milliseconds
        read_noise_electrons (float): Read noise in electrons RMS
        dark_current_e_per_s (float): Dark current in electrons/pixel/second
    
    Returns:
        dict: Complete noise analysis
    """
    import math
    
    # Convert exposure time to seconds
    exposure_time_s = exposure_time_ms / 1000.0
    
    # Calculate dark current electrons
    dark_electrons = dark_current_e_per_s * exposure_time_s
    
    # Calculate individual noise components
    shot_noise = math.sqrt(max(signal_electrons, 0))  # Shot noise from signal
    dark_noise = math.sqrt(max(dark_electrons, 0))    # Shot noise from dark current
    read_noise = read_noise_electrons                  # Read noise (constant)
    
    # Total noise (RSS - Root Sum of Squares)
    total_noise = math.sqrt(signal_electrons + dark_electrons + read_noise**2)
    
    # Signal-to-Noise Ratio
    snr = signal_electrons / total_noise if total_noise > 0 else 0
    snr_db = 20 * math.log10(snr) if snr > 0 else float('-inf')
    
    # Determine noise regime
    noise_regime = determine_noise_regime(signal_electrons, dark_electrons, read_noise)
    
    return {
        'signal_electrons': signal_electrons,
        'dark_electrons': dark_electrons,
        'noise_components': {
            'shot_noise': shot_noise,
            'dark_noise': dark_noise,
            'read_noise': read_noise,
            'total_noise': total_noise
        },
        'snr': {
            'linear': snr,
            'db': snr_db
        },
        'noise_regime': noise_regime,
        'exposure_time_s': exposure_time_s
    }


def determine_noise_regime(signal_electrons, dark_electrons, read_noise):
    """
    Determine which noise source dominates
    
    Args:
        signal_electrons (float): Signal electrons
        dark_electrons (float): Dark current electrons
        read_noise (float): Read noise electrons
    
    Returns:
        str: Dominant noise regime
    """

    import math
    shot_noise = math.sqrt(max(signal_electrons, 0))
    dark_noise = math.sqrt(max(dark_electrons, 0))
    
    # Find the largest noise component
    noise_sources = {
        'shot_limited': shot_noise,
        'dark_limited': dark_noise,
        'read_limited': read_noise
    }
    
    dominant_regime = max(noise_sources, key=noise_sources.get)
    
    # Additional logic for combined regimes
    total_shot_dark = math.sqrt(signal_electrons + dark_electrons)
    if total_shot_dark > read_noise * 2:
        if signal_electrons > dark_electrons * 2:
            return 'shot_limited'
        elif dark_electrons > signal_electrons * 2:
            return 'dark_limited'
        else:
            return 'shot_dark_limited'
    else:
        return 'read_limited'


def calculate_full_chain(scene_illuminance, scene_reflectance, lens_transmittance, 
                        f_number, pixel_size_um, exposure_time_ms, 
                        wavelength_nm, quantum_efficiency, read_noise_electrons=3.0, 
                        dark_current_e_per_s=0.1):
    """
    Complete calculation from scene illumination to electron count with noise analysis
    
    Args:
        scene_illuminance (float): Scene illuminance (lux)
        scene_reflectance (float): Scene reflectance (0-1)
        lens_transmittance (float): Lens transmittance (0-1)
        f_number (float): Lens f-number
        pixel_size_um (float): Pixel size (μm)
        exposure_time_ms (float): Exposure time (ms)
        wavelength_nm (float): Wavelength (nm)
        quantum_efficiency (float): Quantum efficiency (0-1)
        read_noise_electrons (float): Read noise (electrons RMS)
        dark_current_e_per_s (float): Dark current (electrons/pixel/second)
    
    Returns:
        dict: Complete results with intermediate values and noise analysis
    """
    # Step 1: Scene luminance
    scene_luminance = calculate_scene_luminance(scene_illuminance, scene_reflectance)
    
    # Step 2: Sensor illuminance
    sensor_illuminance = calculate_sensor_illuminance(scene_luminance, lens_transmittance, f_number)
    
    # Step 3: Photon count
    photon_count, photon_intermediates = calculate_photon_count(
        sensor_illuminance, pixel_size_um, exposure_time_ms, wavelength_nm
    )
    
    # Step 4: Electron count
    electron_count = calculate_electrons(photon_count, quantum_efficiency)
    
    # Step 5: Noise analysis
    noise_analysis = calculate_noise_analysis(
        electron_count, exposure_time_ms, read_noise_electrons, dark_current_e_per_s
    )
    
    return {
        'inputs': {
            'scene_illuminance_lux': scene_illuminance,
            'scene_reflectance': scene_reflectance,
            'lens_transmittance': lens_transmittance,
            'f_number': f_number,
            'pixel_size_um': pixel_size_um,
            'exposure_time_ms': exposure_time_ms,
            'wavelength_nm': wavelength_nm,
            'quantum_efficiency': quantum_efficiency,
            'read_noise_electrons': read_noise_electrons,
            'dark_current_e_per_s': dark_current_e_per_s
        },
        'results': {
            'scene_luminance_nits': scene_luminance,
            'sensor_illuminance_lux': sensor_illuminance,
            'photon_count': photon_count,
            'electron_count': electron_count
        },
        'noise_analysis': noise_analysis,
        'intermediates': photon_intermediates
    }


def format_results_for_notebook(results):
    """
    Format calculation results for nice display in Jupyter notebook
    
    Args:
        results (dict): Results from calculate_full_chain()
    
    Returns:
        str: Formatted HTML string for notebook display
    """
    from IPython.display import HTML
    
    inputs = results['inputs']
    res = results['results']
    noise = results['noise_analysis']
    inter = results['intermediates']
    
    # Determine regime color coding
    regime_colors = {
        'shot_limited': '#28a745',
        'dark_limited': '#dc3545', 
        'read_limited': '#ffc107',
        'shot_dark_limited': '#17a2b8'
    }
    regime_color = regime_colors.get(noise['noise_regime'], '#6c757d')
    
    html = f"""
    <div style="font-family: 'Courier New', monospace; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6;">
        <h3 style="color: #495057; margin-top: 0;">🔬 Light Calculator Results</h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;">
            <div style="background-color: #e9ecef; padding: 15px; border-radius: 8px;">
                <h4 style="color: #6c757d; margin-top: 0;">⚡ Signal</h4>
                <div style="font-size: 24px; font-weight: bold; color: #198754;">
                    {res['electron_count']:.0f} electrons
                </div>
            </div>
            <div style="background-color: #e9ecef; padding: 15px; border-radius: 8px;">
                <h4 style="color: #6c757d; margin-top: 0;">📊 Signal-to-Noise</h4>
                <div style="font-size: 24px; font-weight: bold; color: #0d6efd;">
                    {noise['snr']['linear']:.1f} ({noise['snr']['db']:.1f} dB)
                </div>
            </div>
        </div>
        
        <h4 style="color: #6c757d;">🔊 Noise Analysis:</h4>
        <div style="background-color: white; padding: 12px; border-radius: 8px; border-left: 4px solid {regime_color};">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center;">
                <div>
                    <strong>Shot Noise</strong><br>
                    <span style="color: #28a745; font-size: 16px;">{noise['noise_components']['shot_noise']:.1f}e⁻</span>
                </div>
                <div>
                    <strong>Dark Noise</strong><br>
                    <span style="color: #dc3545; font-size: 16px;">{noise['noise_components']['dark_noise']:.1f}e⁻</span>
                </div>
                <div>
                    <strong>Read Noise</strong><br>
                    <span style="color: #ffc107; font-size: 16px;">{noise['noise_components']['read_noise']:.1f}e⁻</span>
                </div>
                <div>
                    <strong>Total Noise</strong><br>
                    <span style="color: #6f42c1; font-size: 16px;">{noise['noise_components']['total_noise']:.1f}e⁻</span>
                </div>
            </div>
            <div style="margin-top: 10px; text-align: center;">
                <strong style="color: {regime_color};">Noise Regime: {noise['noise_regime'].replace('_', ' ').title()}</strong>
            </div>
        </div>
        
        <h4 style="color: #6c757d;">🔄 Calculation Steps:</h4>
        <ol style="margin: 10px 0;">
            <li><strong>Scene Luminance:</strong> {res['scene_luminance_nits']:.2f} nits</li>
            <li><strong>Sensor Illuminance:</strong> {res['sensor_illuminance_lux']:.2f} lux</li>
            <li><strong>Photon Count:</strong> {res['photon_count']:.0f} photons/pixel</li>
            <li><strong>Signal Electrons:</strong> {res['electron_count']:.0f} electrons/pixel</li>
            <li><strong>Dark Electrons:</strong> {noise['dark_electrons']:.1f} electrons/pixel</li>
        </ol>
        
        <details style="margin-top: 15px;">
            <summary style="cursor: pointer; color: #6c757d;"><strong>🔍 View Intermediate Values</strong></summary>
            <div style="margin-top: 10px; font-size: 12px;">
                <p><strong>Sensor Irradiance:</strong> {inter['sensor_irradiance_w_per_m2']:.2e} W/m²</p>
                <p><strong>Pixel Area:</strong> {inter['pixel_area_m2']:.2e} m²</p>
                <p><strong>Photon Energy:</strong> {inter['photon_energy_j']:.2e} J</p>
                <p><strong>Exposure Time:</strong> {inter['exposure_time_s']:.3f} s</p>
                <p><strong>Total Energy per Pixel:</strong> {inter['total_energy_per_pixel_j']:.2e} J</p>
            </div>
        </details>
    </div>
    """
    
    return HTML(html)


def get_calculation_data_for_plotting(results):
    """
    Extract data from results for visualization
    
    Args:
        results (dict): Results from calculate_full_chain()
    
    Returns:
        tuple: (step_names, step_values, units)
    """
    res = results['results']
    
    step_names = [
        'Scene\nLuminance',
        'Sensor\nIlluminance', 
        'Photon\nCount',
        'Electron\nCount'
    ]
    
    # Normalize values for plotting (log scale)
    import math
    step_values = [
        math.log10(max(res['scene_luminance_nits'], 1e-10)),
        math.log10(max(res['sensor_illuminance_lux'], 1e-10)),
        math.log10(max(res['photon_count'], 1e-10)),
        math.log10(max(res['electron_count'], 1e-10))
    ]
    
    units = ['nits', 'lux', 'photons', 'electrons']
    
    return step_names, step_values, units