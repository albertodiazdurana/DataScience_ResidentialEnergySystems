# Part I: Domain Fundamentals - Heating Systems & Energy Technology

---

## Chapter 1: Thermodynamic Principles for Heating Systems

Understanding heating system optimization requires a solid foundation in thermodynamics. This chapter establishes the physical principles governing heat transfer, thermal storage, and energy demand estimation in buildings.

### 1.1 Heat Transfer Modes

Heat transfer in buildings occurs through three fundamental mechanisms, each with distinct mathematical descriptions and practical implications for heating system design.

**Conduction** describes heat flow through solid materials. The rate of conductive heat transfer through a building element (wall, window, roof) follows Fourier's Law:

$$\dot{Q}_{cond} = \frac{\lambda \cdot A \cdot \Delta T}{d}$$

Where λ is thermal conductivity (W/m·K), A is surface area (m²), ΔT is temperature difference (K), and d is material thickness (m). For building components, we use the U-value (thermal transmittance, W/m²·K), which incorporates multiple material layers and surface resistances:

$$\dot{Q} = U \cdot A \cdot (T_{inside} - T_{outside})$$

A typical uninsulated 1970s building in Germany might have wall U-values of 1.5-2.0 W/m²·K, while modern KfW-70 standards require approximately 0.2-0.3 W/m²·K. This order-of-magnitude difference explains why the dhu Hamburg case study achieved only 8% additional savings on a KfW-70 building versus 18% on poorly optimized older stock.

**Convection** transfers heat between surfaces and moving fluids (air or water). The convective heat transfer rate is:

$$\dot{Q}_{conv} = h \cdot A \cdot (T_{surface} - T_{fluid})$$

The convective heat transfer coefficient h (W/m²·K) depends on fluid velocity, geometry, and flow regime. In hydronic heating systems, forced convection in pipes achieves h values of 500-10,000 W/m²·K, enabling efficient heat transport from boiler to radiators.

**Radiation** follows the Stefan-Boltzmann law. For building surfaces exchanging thermal radiation:

$$\dot{Q}_{rad} = \varepsilon \cdot \sigma \cdot A \cdot (T_1^4 - T_2^4)$$

Where ε is emissivity (0-1), σ is the Stefan-Boltzmann constant (5.67×10⁻⁸ W/m²·K⁴), and temperatures are in Kelvin. Radiative losses through windows and from building envelopes contribute significantly to heating demand, particularly at night.

### 1.2 Thermal Mass and Building Inertia

Buildings store thermal energy in their structural mass (concrete, brick, water in heating systems). This thermal capacitance creates temporal dynamics critical for control optimization.

The thermal time constant τ characterizes how quickly a building responds to temperature changes:

$$\tau = \frac{C_{thermal}}{UA_{total}}$$

Where C_thermal is the building's heat capacity (J/K) and UA_total is the total heat loss coefficient (W/K). Heavy masonry buildings common in German housing stock may have time constants of 20-50 hours, meaning temperature changes propagate slowly.

This inertia has practical implications for Green Fusion's optimization strategies. A building with high thermal mass can be "pre-heated" during periods of cheap electricity (for heat pumps) or high PV production, storing thermal energy for later use. The system can coast through peak demand periods without active heating, enabling peak shaving strategies that reduce Anschlussleistung costs in district heating systems.

### 1.3 Degree-Day Calculations and Heating Load Estimation

**Heating Degree Days (HDD)** quantify the heating demand over time. For a given day:

$$HDD = max(0, T_{base} - T_{avg,outdoor})$$

The base temperature T_base (typically 15-18°C in Germany) represents the outdoor temperature below which heating is required. Annual HDD values vary geographically: Berlin averages approximately 3,000-3,200 Kd (Kelvin-days), while Munich sees 3,500-3,800 Kd due to its more continental climate.

**Heating load calculation** (Heizlastberechnung) per DIN EN 12831 determines the maximum power required to maintain indoor comfort during design conditions. The transmission heat loss is:

$$\Phi_T = \sum_i (U_i \cdot A_i) \cdot (T_{int} - T_{ext,design})$$

For Berlin, the design outdoor temperature is approximately -14°C. With an indoor setpoint of 20°C, ΔT = 34K. A building with UA_total = 500 W/K would require:

$$\Phi_T = 500 \cdot 34 = 17,000 W = 17 kW$$

Adding ventilation losses (typically 20-40% of transmission losses) yields the total heating load. This calculation underpins the Verfahren B hydraulic balancing methodology discussed in Chapter 4.

---

## Chapter 2: Heating System Types & Control Parameters

Green Fusion's platform operates across heterogeneous heating technologies. Each system type has distinct efficiency characteristics, control interfaces, and optimization opportunities.

### 2.1 Gas and Oil Boilers

Conventional boilers remain dominant in German residential buildings, with approximately 50% of apartments heated by gas. Two efficiency metrics are relevant:

**Lower heating value (LHV) efficiency** measures useful heat output relative to fuel chemical energy, excluding latent heat of water vapor in combustion products. Older atmospheric boilers achieve 80-85% LHV efficiency.

**Condensing efficiency (Brennwertnutzung)** recovers latent heat by cooling flue gases below the water vapor dew point (~57°C for natural gas). Condensing boilers can exceed 100% LHV efficiency (typically 104-109%) by capturing this additional energy.

The critical insight: condensing only occurs when return water temperature is sufficiently low (below ~55°C). Green Fusion's optimization of Rücklauftemperatur directly increases Brennwertnutzung. In the DIE EHRENFELDER case study, reducing return temperatures and optimizing boiler sequencing improved condensing operation significantly.

**Boiler cascade control** (Kesselfolgeschaltung) in multi-boiler installations determines which units fire and in what sequence. Optimal strategies minimize cycling (Taktverhalten), maintain each boiler in its efficient operating range, and maximize condensing operation. The case study revealed all boilers running simultaneously even in summer, a classic control fault.

### 2.2 District Heating (Fernwärme)

District heating serves approximately 14% of German households, with higher penetration in urban multi-family housing. The economic structure differs fundamentally from fuel-based systems.

**Cost components:**
- Grundpreis (base cost): proportional to contracted Anschlussleistung (kW)
- Arbeitspreis (consumption cost): per kWh delivered
- Return temperature penalties: surcharges when Rücklauf exceeds contractual limits (typically 50-60°C)

**Optimization opportunities:**

The WSL Leipzig case study achieved 16.5% savings through several mechanisms. First, dynamic Heizkennlinie adjustment reduced flow temperatures while maintaining comfort. Second, coordinated control prevented simultaneous heating and DHW peaks that drive up measured Anschlussleistung. Third, continuous monitoring ensured return temperatures stayed below penalty thresholds.

**Spreizung** (temperature spread) between Vorlauf and Rücklauf indicates heat extraction efficiency. Higher spreizung means more energy extracted per unit water flow, reducing pumping energy and improving system efficiency. Typical target: ΔT ≥ 20-30K.

### 2.3 Heat Pumps

Heat pumps transfer thermal energy from a low-temperature source (air, ground, water) to the building's heating system. Their efficiency is characterized by the Coefficient of Performance (COP):

$$COP = \frac{\dot{Q}_{heating}}{\dot{W}_{electrical}}$$

Modern heat pumps achieve COP values of 3-5, meaning 3-5 kWh of heat delivered per kWh of electricity consumed. The theoretical maximum (Carnot COP) depends only on temperatures:

$$COP_{Carnot} = \frac{T_{hot}}{T_{hot} - T_{cold}}$$

With T_hot = 35°C (308K, low-temperature heating) and T_cold = 0°C (273K, winter air source):

$$COP_{Carnot} = \frac{308}{308 - 273} = 8.8$$

Real heat pumps achieve 40-60% of Carnot efficiency. The key optimization insight: COP improves dramatically with lower flow temperatures and higher source temperatures. Reducing Vorlauftemperatur from 55°C to 35°C can improve COP by 30-50%.

**Source types:**
- Air-source (Luft-Wärmepumpe): lowest installation cost, COP varies significantly with outdoor temperature
- Ground-source (Erdwärmepumpe): stable COP year-round, higher installation cost
- Water-source: highest COP potential, limited applicability

### 2.4 Combined Heat and Power (BHKW)

Blockheizkraftwerke simultaneously generate electricity and useful heat from fuel combustion. Key metrics:

**Electrical efficiency** (η_el): typically 25-40% for small-scale units
**Thermal efficiency** (η_th): typically 50-65%
**Total efficiency**: η_el + η_th = 85-95%

**Stromkennzahl** (power-to-heat ratio) = η_el / η_th indicates the relative output balance. Values range from 0.4-0.8 for typical residential BHKW.

Optimization focuses on heat-led operation, running the BHKW when heat is needed and electricity is valuable. Active Speichermanagement buffers thermal output, allowing electrical generation to follow grid demand or price signals.

### 2.5 Hybrid and Multivalent Systems

Modern installations increasingly combine multiple heat sources. The GWU Eckernförde case study featured two heat pumps with auxiliary electric heating. The challenge: preventing inefficient backup systems from dominating operation.

Analysis revealed the Durchlauferhitzer (instantaneous water heater) running excessively, bypassing the more efficient heat pumps. Optimization reduced hot water electricity consumption by 20% by coordinating heat pump operation and minimizing auxiliary heater runtime.

Hybrid systems require holistic control strategies that consider:
- Source availability and efficiency (COP varies with conditions)
- Electricity prices (dynamic tariffs favor flexible loads)
- Thermal storage state (buffer tanks, building mass)
- Comfort constraints (minimum temperatures, DHW availability)

---

## Chapter 3: Key Control Variables

This chapter details the specific parameters that Green Fusion's Energiespar-Pilot optimizes. Understanding these variables is essential for developing and explaining optimization algorithms.

### 3.1 Heizkennlinie (Heating Curve)

The Heizkennlinie defines the relationship between outdoor temperature and heating system flow temperature. It is the single most impactful control parameter for heating efficiency.

**Mathematical representation:**

$$T_{Vorlauf} = T_{setpoint} + K \cdot (T_{room,target} - T_{outdoor})^{n}$$

Where K is the curve slope (Steilheit) and n is typically 1.0-1.5. A simpler linear approximation:

$$T_{Vorlauf} = T_{base} - m \cdot T_{outdoor}$$

**Optimization approach:**

Green Fusion's analysis of 800 heating systems found average Vorlauftemperatur of 64.4°C at 4°C outdoor temperature, far exceeding actual requirements. Optimal curves deliver minimum flow temperature that maintains comfort.

Adjustments include:
- **Slope reduction**: lower temperatures at mild outdoor conditions
- **Parallel shift**: uniform reduction across all outdoor temperatures
- **Endpoint adjustment**: maximum temperature at design conditions

Iterative optimization starts conservatively and reduces temperatures in steps, monitoring comfort feedback. The 4-week analysis phase establishes baseline behavior before modifications.

### 3.2 Vorlauf- und Rücklauftemperatur

**Vorlauftemperatur** (flow temperature) directly impacts:
- Distribution losses (proportional to ΔT from ambient)
- Condensing boiler efficiency (requires return < 55°C)
- Heat pump COP (lower is better)
- Legionella risk in DHW systems (minimum 60°C at tank)

**Rücklauftemperatur** determines heat extraction efficiency. The relationship:

$$\dot{Q} = \dot{m} \cdot c_p \cdot (T_{Vorlauf} - T_{Rücklauf})$$

For fixed heat demand Q̇, lower Rücklauf requires lower mass flow ṁ (reduced pumping energy) or allows lower Vorlauf (reduced losses).

District heating contracts often specify maximum Rücklauftemperatur (50-60°C). Violations trigger penalties. Green Fusion monitors this continuously, adjusting Heizkennlinie parameters to maintain compliance.

### 3.3 Hysteresis

Hysteresis defines the temperature band around setpoints that triggers heating system cycling. Example: a 3K hysteresis on a 60°C tank setpoint means heating activates at 57°C and deactivates at 63°C.

**Too narrow hysteresis** causes excessive cycling (Taktverhalten), increasing:
- Component wear (valve actuators, igniters, compressors)
- Standby losses during off-cycles
- Efficiency losses from transient operation

**Too wide hysteresis** causes:
- Comfort variations (temperature swings)
- Overshooting (wasted energy)

Optimization balances cycling frequency against temperature stability. For boilers, typical targets are 3-6 cycles per hour maximum. Heat pump compressors prefer even fewer cycles due to high start-up currents.

### 3.4 Speicher-Solltemperatur (Storage Setpoint)

Buffer tanks (Pufferspeicher) and DHW tanks have temperature setpoints affecting system efficiency.

**DHW storage** (Trinkwarmwasserspeicher) must balance:
- Legionella prevention: minimum 60°C storage, 55°C distribution
- Energy efficiency: lower temperatures reduce standby losses
- User comfort: adequate hot water availability

Green Fusion data revealed 20% of systems with storage temperatures exceeding 65°C unnecessarily. Reducing to 60°C while ensuring periodic thermal disinfection (Legionellenschaltung) captures significant savings.

**Buffer tanks** in heat pump systems store thermal energy for:
- Bridging defrost cycles (air-source heat pumps)
- Load shifting to favorable electricity prices
- Reducing compressor cycling

Optimal setpoints depend on usage patterns, identified through data analysis.

### 3.5 Night Setback and Summer Mode

**Nachtabsenkung** (night setback) reduces heating during low-occupancy periods. The Green Fusion dataset showed 70% of systems operating without night setback, representing immediate optimization potential.

Implementation considerations:
- Building thermal mass determines optimal setback depth and timing
- Morning warm-up must avoid creating demand peaks (Fernwärme Anschlussleistung)
- Setback timing should anticipate occupancy, not react to it

**Summer mode** (Sommerbetrieb) disables space heating when outdoor temperatures exceed a threshold (typically 15-18°C). Automatic switching based on weather data and building response prevents unnecessary heating in shoulder seasons.

---

## Chapter 4: Hydraulic Balancing (Hydraulischer Abgleich)

Hydraulic balancing ensures each heating circuit receives its design water flow rate. This chapter examines when balancing is necessary and the methods for achieving it.

### 4.1 The Hydraulic Problem

Hydronic heating systems distribute hot water through pipes to radiators or floor heating circuits. Without balancing, water preferentially flows through paths of least resistance (nearest radiators, largest pipes), starving distant or restricted circuits.

Symptoms of poor hydraulic balance:
- Temperature disparities between rooms/apartments
- Noise from high-velocity flow in some circuits
- Inability to reduce flow temperatures (distant radiators underperform)
- Pump operating at excessive pressure to compensate

### 4.2 Verfahren A vs. Verfahren B

German regulations distinguish two balancing methodologies:

**Verfahren A (Simplified)**

Uses tabulated values and building type assumptions to estimate heat loads. Implementation:
1. Estimate room heat loads from building age and type tables
2. Calculate required radiator flow rates
3. Set thermostatic valve presettings accordingly

Limitations: Assumptions may poorly match actual building conditions. Green Fusion considers Verfahren A unreliable for achieving real efficiency gains.

**Verfahren B (Detailed)**

Room-by-room heat load calculation per DIN EN 12831:
1. Survey each room: dimensions, window areas, wall constructions, orientation
2. Calculate transmission and ventilation losses for design conditions
3. Determine required radiator output and flow rate
4. Set valve presettings based on calculated values
5. Commission with measured flow verification

Verfahren B is mandatory for new and modernized systems since 2023. While more expensive and time-consuming (requires access to all units), it delivers reliable results.

### 4.3 Data-Driven Assessment

Green Fusion's approach uses operational data to assess hydraulic balance before recommending physical intervention.

**Diagnostic indicators:**
- Spreizung variation across circuits (balanced systems show uniform ΔT)
- Return temperature patterns (unbalanced systems show short-circuiting)
- Comfort complaints correlated with circuit position

**Analysis findings from 800 systems:**
- 17.5% urgently require hydraulic balancing
- 43% show no significant hydraulic issues
- Remaining 40% may benefit, but operational optimization delivers faster ROI

The recommended sequence:
1. Digitalize and analyze (4-week baseline)
2. Optimize control parameters (immediate savings)
3. Assess residual hydraulic issues from data
4. Target physical balancing where data indicates necessity

This prioritization ensures capital is deployed where impact is highest.

---

## Chapter 5: Sector Coupling (Sektorkopplung)

Sector coupling integrates electricity and heat systems, enabling renewable energy to decarbonize building heating. This chapter examines the technical and optimization challenges.

### 5.1 The Integration Challenge

Traditional buildings consumed fuel (gas, oil) for heat and grid electricity for other loads, with no interaction between sectors. Sector coupling creates interdependencies:

- Heat pumps convert electricity to heat
- PV generates on-site electricity
- Batteries store electrical energy
- Building mass stores thermal energy
- Dynamic tariffs create time-varying electricity costs

Optimizing these coupled systems requires simultaneous consideration of electrical and thermal domains.

### 5.2 PV and Heat Pump Orchestration

The fundamental challenge: temporal mismatch between PV production and heat demand.

**PV production profile:** Peak generation occurs midday (11:00-15:00), with zero output overnight and reduced output in winter.

**Heat demand profile:** Peaks occur morning (06:00-09:00) and evening (17:00-22:00), precisely when PV production is low or zero.

**Optimization strategies:**

**Thermal storage shifting:** Pre-heat DHW tanks and buffer storage during midday PV surplus. The building's thermal mass provides additional storage. With τ = 30 hours, a building can be heated at noon and coast through evening peak demand.

**Battery arbitrage:** Store midday PV surplus in batteries for evening heat pump operation. Economics depend on battery costs, degradation, and alternative revenue (grid feed-in tariffs).

**Predictive control:** Weather forecasts enable proactive optimization. If tomorrow is sunny, minimize overnight heating and plan midday heat pump operation. If cloudy, shift consumption to overnight wind power (via dynamic tariffs).

### 5.3 Dynamic Electricity Pricing

Time-of-use and real-time pricing expose consumers to wholesale market signals. German spot prices vary from negative (renewable oversupply) to >€0.50/kWh (peak demand, low wind/sun).

Heat pumps with storage become valuable flexible loads:
- Consume during price troughs (negative prices = paid to consume)
- Avoid consumption during price spikes
- Provide implicit grid services through demand response

Optimization requires:
- Price forecasts (day-ahead market known at 12:00 prior day)
- Heat demand forecasts (weather-dependent)
- Storage state tracking (thermal and electrical)
- Comfort constraint enforcement

The objective function balances:

$$\min \sum_t \left[ P_{elec}(t) \cdot c(t) + \lambda_{comfort} \cdot violation(t) \right]$$

Where P_elec is electricity consumption, c(t) is time-varying price, and the second term penalizes comfort violations.

### 5.4 Self-Consumption Maximization

Without storage, PV self-consumption in residential buildings typically reaches 20-30%. Adding heat pump flexibility increases this to 40-60%. Batteries push further to 60-80%.

**Self-consumption ratio:**

$$SCR = \frac{E_{PV,self-consumed}}{E_{PV,total}}$$

**Self-sufficiency ratio:**

$$SSR = \frac{E_{PV,self-consumed}}{E_{demand,total}}$$

Optimization targets vary by economic context:
- High feed-in tariffs → prioritize grid export
- Low feed-in tariffs → maximize self-consumption
- Dynamic tariffs → optimize against price signals

Green Fusion's Energiespar-Pilot implements holistic optimization across these dimensions, coordinating heat pump scheduling, storage charging, and heating curve adjustments to maximize economic and environmental outcomes.

### 5.5 System Complexity and Control Requirements

The OSTLAND case study emphasized that hybrid systems cannot be efficiently operated without active intelligent control. The quote bears repeating: "Hybridanlagen können ohne aktive Steuerung nicht effizient betrieben werden."

Manual control cannot respond to:
- 15-minute resolution price signals
- Weather forecast updates
- Real-time PV production variations
- Changing occupancy patterns

Automated, AI-driven control is not a luxury but a necessity for sector-coupled systems to deliver their economic and environmental potential.

---

*End of Part I*
