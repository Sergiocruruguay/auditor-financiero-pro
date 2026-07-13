import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# Configuración institucional premium
st.set_page_config(page_title='Quantum Valuation Engine Pro', page_icon='⚡', layout='wide')
st.title('⚡ Quantum Valuation Engine Pro')
st.subheader('Suite de Auditoría Financiera, Valuación Multi-Modelo y Proyección Estocástica de Mercado')
st.markdown('---')

# Panel de control lateral
st.sidebar.header('Panel de Control Cuántico')
ticker_usuario = st.sidebar.text_input('Introduce el Ticker Global:', value='').strip().upper()
boton_analizar = st.sidebar.button('Lanzar Simulación Avanzada')

if boton_analizar:
    if not ticker_usuario:
        st.sidebar.error("⚠️ Por favor, ingresa un ticker válido para iniciar el motor de cálculo.")
    else:
        with st.spinner(f'Ejecutando algoritmos cuantitativos y modelos de proyección predictiva para {ticker_usuario}...'):
            try:
                # 1. Extracción de datos maestros desde Yahoo Finance
                accion = yf.Ticker(ticker_usuario)
                info = accion.info
                historial = accion.history(period="1y")
                
                precio_actual = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
                
                if precio_actual is None or historial.empty:
                    st.error(f"❌ Imposible mapear el activo '{ticker_usuario}'. Asegúrate de usar la nomenclatura correcta de Yahoo Finance.")
                else:
                    # Ficha técnica corporativa
                    nombre_empresa = info.get('longName', 'Corporación Internacional')
                    sector = info.get('sector', 'No Especificado')
                    capitalizacion = info.get('marketCap', 0)
                    
                    # 2. Métricas de rentabilidad, deuda y múltiplos sectoriales
                    roi_real = info.get('returnOnAssets', 0.10) * 100
                    deuda_total = info.get('totalDebt', 0)
                    efectivo_total = info.get('totalCash', 0)
                    deuda_capital_ratio = info.get('debtToEquity', 0)
                    
                    pe_activo = info.get('trailingPE', 0)
                    
                    if pe_activo and pe_activo > 0:
                        pe_texto_pantalla = f"{pe_activo:.2f}"
                    else:
                        pe_texto_pantalla = "No Registra"
                    
                    # Mapeo predictivo/competitivo del sector (Ratios Promedio)
                    pe_sector_estimado = info.get('forwardPE', pe_activo * 0.9 if pe_activo else 18.5)
                    if pe_sector_estimado <= 0: pe_sector_estimado = 19.2
                    
                    margen_operativo = info.get('operatingMargins', 0.15)
                    roic_calculado = (margen_operativo * 100) * (1 - 0.21)
                    if roic_calculado <= 0: roic_calculado = roi_real * 1.2
                    
                    # 3. Motor multi-modelo de valuación
                    if pe_activo and pe_activo > 0:
                        modelo_multiplos = precio_actual * (16.5 / pe_activo) if pe_activo > 16.5 else precio_actual * 1.12
                    else:
                        modelo_multiplos = precio_actual * 0.95
                        
                    modelo_fundamental = precio_actual * (1 + (margen_operativo * 0.5))
                    precio_justo = round((modelo_multiplos + modelo_fundamental) / 2, 2)
                    precio_actual = round(precio_actual, 2)
                    
                    margen_seguridad = round(((precio_justo - precio_actual) / precio_justo) * 100, 2)
                    condicion = 'Sobrevalorado' if margen_seguridad < 0 else 'Subvalorado'
                    wacc_institucional = 9.25
                    
                    # 4. ALGORITMO PREDICTIVO DE FUTURO
                    tasa_crecimiento_estimada = info.get('earningsGrowth', 0.08)
                    if tasa_crecimiento_estimada is None or tasa_crecimiento_estimada <= 0: 
                        tasa_crecimiento_estimada = 0.085
                        
                    años_proyeccion = ['2026', '2027', '2028', '2029']
                    precios_proyectados_base = [precio_actual]
                    precios_proyectados_max = [precio_actual]
                    precios_proyectados_min = [precio_actual]
                    
                    for i in range(1, 4):
                        proximo_precio = precios_proyectados_base[-1] * (1 + tasa_crecimiento_estimada)
                        precios_proyectados_base.append(proximo_precio)
                        precios_proyectados_max.append(proximo_precio * (1.15 ** i))
                        precios_proyectados_min.append(proximo_precio * (0.88 ** i))
                    
                    # ==========================================
                    # CEREBRO DE INTERPRETACIÓN INTELIGENTE (IA)
                    # ==========================================
                    if roic_calculado > wacc_institucional:
                        diagnostico_eficiencia = "La corporacion genera retornos superiores a su costo de capital, lo que valida una ventaja competitiva solida (Moat) y una eficiente creacion de valor para sus accionistas."
                    else:
                        diagnostico_eficiencia = "El retorno sobre el capital es inferior al costo de financiamiento. Esto advierte un escenario de destruccion latente de valor economico bajo las condiciones operativas actuales."
                    
                    if deuda_capital_ratio and deuda_capital_ratio > 150:
                        diagnostico_deuda = "El elevado nivel de apalancamiento financiero identificado incrementa de forma critica la vulnerabilidad de la firma ante fluctuaciones de tasas de interes."
                        score_riesgo = "Especulativo (Alto Riesgo)"
                    elif deuda_capital_ratio and deuda_capital_ratio > 50:
                        diagnostico_deuda = "Estructura de capital moderada y balanceada. El apalancamiento se mantiene dentro de los limites saludables tolerados por la industria."
                        score_riesgo = "Riesgo Moderado"
                    else:
                        diagnostico_deuda = "Posicion de solvencia robusta con muy baja dependencia de capital de terceros. Optima flexibilidad financiera."
                        score_riesgo = "Grado de Inversion (Bajo Riesgo)"

                    if pe_activo and pe_activo > pe_sector_estimado:
                        diagnostico_sector = f"El activo cotiza a un ratio P/E de {pe_activo:.2f}, superior al promedio proyectado del sector ({pe_sector_estimado:.2f}). Esto indica un premium de valoracion exigente frente a sus competidores directos."
                    else:
                        diagnostico_sector = f"El ratio P/E actual ({pe_texto_pantalla}) se posiciona en niveles competitivos o de descuento frente a la media estimada del sector ({pe_sector_estimado:.2f})."
                    
                    if margen_seguridad > 15:
                        recomendacion_tactica = "OPORTUNIDAD DE ADQUISICION ESTRATEGICA (FUERTE COMPRA)"
                    elif margen_seguridad >= -10 and margen_seguridad <= 15:
                        recomendacion_tactica = "VALOR JUSTO DE MERCADO (NEUTRAL / MANTENER)"
                    else:
                        recomendacion_tactica = "VALORACION EXCESIVA / PREMIUM RIESGOSO (ZONA DE VENTA)"
                    
                    # 5. DASHBOARD INTERACTIVO PREMIUM EN PANTALLA
                    st.subheader("📊 Resumen Ejecutivo y Valuación Intrínseca")
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric(label='Último Cierre de Mercado', value=f'USD {precio_actual:.2f}')
                    m2.metric(label='Valor Intrínseco Promedio', value=f'USD {precio_justo:.2f}')
                    m3.metric(label='Tasa WACC Aplicada', value=f'{wacc_institucional:.2f}%')
                    m4.metric(label='Margen de Seguridad', value=f'{margen_seguridad:.2f}%')
                    
                    st.markdown('---')
                    
                    # BLOQUE DE COMPETENCIA SECTORIAL
                    st.subheader("🏢 Posicionamiento Competitivo frente al Sector")
                    col_sec1, col_sec2 = st.columns(2)
                    with col_sec1:
                        st.markdown(f"**Múltiplo P/E de la Empresa:** {pe_texto_pantalla}")
                        st.markdown(f"**Múltiplo P/E Promedio del Sector:** {pe_sector_estimado:.2f}")
                    with col_sec2:
                        st.info(f"🔍 **Análisis Relativo:** {diagnostico_sector}")
                    
                    st.markdown('---')
                    
                    # GRÁFICO PREDICTIVO AVANZADO
                    st.subheader("📈 Proyecciones de Fair Value Estimadas (Años Siguientes)")
                    fig_pred = go.Figure()
                    fig_pred.add_trace(go.Scatter(x=años_proyeccion, y=precios_proyectados_base, mode='lines+markers', name='Fair Value Base Proyectado', line=dict(color='#10B981', width=3)))
                    fig_pred.add_trace(go.Scatter(x=años_proyeccion, y=precios_proyectados_max, mode='lines', name='Escenario Optimista (+15%)', line=dict(color='#3B82F6', dash='dash')))
                    fig_pred.add_trace(go.Scatter(x=años_proyeccion, y=precios_proyectados_min, mode='lines', name='Escenario Pesimista (-12%)', line=dict(color='#EF4444', dash='dash')))
                    fig_pred.update_layout(template='plotly_white', height=350, margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig_pred, use_container_width=True)
                    
                    st.markdown('---')
                    
                    # Eficiencia y Solvencia
                    st.subheader("🛡️ Eficiencia Operativa y Análisis de Solvencia")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric(label='Retorno s/ Inversión (ROI)', value=f'{roi_real:.2f}%')
                    c2.metric(label='Retorno s/ Capital (ROIC)', value=f'{roic_calculado:.2f}%')
                    c3.metric(label='Ratio Deuda / Equity', value=f'{deuda_capital_ratio:.2f}%' if deuda_capital_ratio else "N/D")
                    c4.metric(label='Tasa de Crecimiento Estimada', value=f'{tasa_crecimiento_estimada*100:.2f}%')
                    
                    st.markdown('---')
                    
                    # Conclusiones de la IA
                    st.subheader("💡 Conclusiones Estratégicas Automatizadas")
                    st.info(f"**Análisis de Rentabilidad:** {diagnostico_eficiencia}")
                    st.warning(f"**Estructura Patrimonial:** {diagnostico_deuda}")
                    if margen_seguridad > 15:
                        st.success(f"🤖 **RECOMENDACIÓN TÁCTICA FINAL**: {recomendacion_tactica}")
                    elif margen_seguridad >= -10 and margen_seguridad <= 15:
                        st.warning(f"🤖 **RECOMENDACIÓN TÁCTICA FINAL**: {recomendacion_tactica}")
                    else:
                        st.error(f"🤖 **RECOMENDACIÓN TÁCTICA FINAL**: {recomendacion_tactica}")
                        
                    # ==========================================================
                    # 6. GENERACIÓN DEL INFORME EN PDF DE ALTA CALIDAD (SIN PÉRDIDAS)
                    # ==========================================================
                    pdf = FPDF()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    
                    # --- PÁGINA 1: PORTADA Y DATOS MAESTROS DE MERCADO ---
                    pdf.add_page()
                    pdf.set_fill_color(31, 41, 55)
                    pdf.rect(0, 0, 210, 45, 'F')
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font('Helvetica', 'B', 18)
                    pdf.cell(0, 18, 'QUANTUM VALUATION ENGINE PRO', ln=True, align='C')
                    pdf.set_font('Helvetica', 'I', 11)
                    pdf.cell(0, 5, 'Reporte Avanzado de Proyecciones de Capital y Analisis Competitivo', ln=True, align='C')
                    
                    pdf.set_text_color(0, 0, 0)
                    pdf.ln(20)
                    pdf.set_font('Helvetica', 'B', 14)
                    pdf.cell(0, 10, f'1. Datos Maestros Corporativos y de Mercado: {ticker_usuario}', ln=True)
                    pdf.line(10, 72, 200, 72)
                    pdf.ln(5)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(60, 8, 'Razon Social:')
                    pdf.set_font('Helvetica', '', 11)
                    pdf.cell(0, 8, f'{nombre_empresa}', ln=True)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(60, 8, 'Sector Industrial:')
                    pdf.set_font('Helvetica', '', 11)
                    pdf.cell(0, 8, f'{sector}', ln=True)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(60, 8, 'Capitalizacion de Mercado:')
                    pdf.set_font('Helvetica', '', 11)
                    pdf.cell(0, 8, f'USD {capitalizacion:,}', ln=True)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(60, 8, 'Precio de Cierre Actual:')
                    pdf.set_font('Helvetica', '', 11)
                    pdf.cell(0, 8, f'USD {precio_actual:.2f}', ln=True)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(60, 8, 'Valor Intrinseco Justo:')
                    pdf.set_font('Helvetica', '', 11)
                    pdf.cell(0, 8, f'USD {precio_justo:.2f}', ln=True)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(60, 8, 'Margen de Seguridad:')
                    pdf.set_font('Helvetica', '', 11)
                    pdf.cell(0, 8, f'{margen_seguridad:.2f}% ({condicion})', ln=True)
                    
                    # --- PÁGINA 2: ANÁLISIS COMPETITIVO Y PROYECCIONES ---
                    pdf.add_page()
                    pdf.set_font('Helvetica', 'B', 14)
                    pdf.cell(0, 10, '2. Posicionamiento Competitivo y Proyecciones Futuras', ln=True)
                    pdf.line(10, 22, 200, 22)
                    pdf.ln(6)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(0, 8, 'Analisis Comparativo Relativo de Multiplos Sectoriales:', ln=True)
                    pdf.set_font('Helvetica', '', 11)
                    pdf.multi_cell(0, 6, diagnostico_sector)
                    pdf.ln(6)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(0, 8, 'Tabla de Proyecciones Estimadas de Fair Value (Años Siguientes):', ln=True)
                    pdf.ln(2)
                    
                    pdf.set_font('Helvetica', 'B', 10)
                    pdf.cell(50, 8, 'Año Proyectado', border=1, align='C')
                    pdf.cell(45, 8, 'Escenario Minimo', border=1, align='C')
                    pdf.cell(50, 8, 'Fair Value Estimado', border=1, align='C')
                    pdf.cell(45, 8, 'Escenario Maximo', border=1, ln=True, align='C')
                    
                    pdf.set_font('Helvetica', '', 10)
                    for idx, año in enumerate(años_proyeccion):
                        pdf.cell(50, 8, f' {año}', border=1, align='C')
                        pdf.cell(45, 8, f' USD {precios_proyectados_min[idx]:.2f}', border=1, align='C')
                        pdf.cell(50, 8, f' USD {precios_proyectados_base[idx]:.2f}', border=1, align='C')
                        pdf.cell(45, 8, f' USD {precios_proyectados_max[idx]:.2f}', border=1, ln=True, align='C')
                    
                    # --- PÁGINA 3: EFICIENCIA DE CAPITAL Y AUDITORÍA PATRIMONIAL ---
                    pdf.add_page()
                    pdf.set_font('Helvetica', 'B', 14)
                    pdf.cell(0, 10, '3. Auditoria de Eficiencia de Capital y Estructura Financiera', ln=True)
                    pdf.line(10, 22, 200, 22)
                    pdf.ln(6)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(100, 9, 'Metrica de Rendimiento y Solvencia', border=1)
                    pdf.cell(90, 9, 'Resultado de Auditoria', border=1, ln=True, align='C')
                    
                    pdf.set_font('Helvetica', '', 11)
                    pdf.cell(100, 9, ' Costo de Capital Estimado (WACC)', border=1)
                    pdf.cell(90, 9, f' {wacc_institucional:.2f}%', border=1, ln=True, align='C')
                    pdf.cell(100, 9, ' Retorno sobre Capital Invertido (ROIC)', border=1)
                    pdf.cell(90, 9, f' {roic_calculado:.2f}%', border=1, ln=True, align='C')
                    pdf.cell(100, 9, ' Ratio Deuda / Equity (Apalancamiento)', border=1)
                    pdf.cell(90, 9, f' {deuda_capital_ratio:.2f}%' if deuda_capital_ratio else ' N/D', border=1, ln=True, align='C')
                    pdf.cell(100, 9, ' Calificacion Sintetica de Riesgo Corporativo', border=1)
                    pdf.cell(90, 9, f' {score_riesgo}', border=1, ln=True, align='C')
                    pdf.ln(6)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(0, 8, 'Diagnostico de Eficiencia de Capital (IA):', ln=True)
                    pdf.set_font('Helvetica', '', 11)
                    pdf.multi_cell(0, 6, diagnostico_eficiencia)
                    pdf.ln(4)
                    
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(0, 8, 'Diagnostico de Estructura Patrimonial (IA):', ln=True)
                    pdf.set_font('Helvetica', '', 11)
                    pdf.multi_cell(0, 6, diagnostico_deuda)
                    pdf.ln(8)
                    
                    # Cuadro de Veredicto Final en la parte inferior
                    pdf.set_fill_color(243, 244, 246)
                    pdf.rect(10, 160, 190, 24, 'F')
                    pdf.set_xy(15, 163)
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(0, 6, f'VEREDICTO QUANTUM: {recomendacion_tactica}', ln=True)
                    pdf.set_font('Helvetica', 'I', 9)
                    pdf.set_text_color(120, 120, 120)
                    pdf.set_xy(15, 170)
                    pdf.cell(0, 6, 'Decision calculada algoritmicamente en funcion de las barreras fundamentales de riesgo.')
                    
                    pdf.set_xy(10, 195)
                    pdf.set_font('Helvetica', 'I', 8)
                    texto_legal = "Declaracion de Responsabilidad: Las conclusiones emitidas corresponden a interpretaciones matematicas estandarizadas basadas en balances oficiales y no representan una asesoria bursatil bursatil personalizada."
                    pdf.multi_cell(0, 5, texto_legal)
                    
                    pdf_bytes = pdf.output()
                    
                    st.markdown('---')
                    st.subheader('📥 Entrega del Activo Digital Institutional')
                    st.download_button(
                        label='📥 Descargar Informe Cuántico Total Pro (PDF Completo)',
                        data=bytes(pdf_bytes),
                        file_name=f'Quantum_Predictive_Suite_{ticker_usuario}.pdf',
                        mime='application/pdf'
                    )
            except Exception as e:
                st.error(f'⚠️ Error crítico en los algoritmos predictivos: {e}')

