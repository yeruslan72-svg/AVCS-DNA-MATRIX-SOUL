    # Sidebar and controls
    st.sidebar.header("🎛️ AVCS DNA Control Panel v6.0")
    
    # System control buttons
    control_col1, control_col2 = st.sidebar.columns(2)
    with control_col1:
        if st.button("⚡ Start System", type="primary", use_container_width=True):
            st.session_state.system_running = True
            # Reset data for new session
            st.session_state.data_dict = {
                'vibration': pd.DataFrame(),
                'temperature': pd.DataFrame(), 
                'noise': pd.DataFrame(columns=['NOISE']),
                'dampers': pd.DataFrame(),
                'risk_history': []
            }
            st.session_state.performance_metrics.update({
                'cycles_completed': 0,
                'emergency_stops': 0,
                'prevented_failures': 0
            })
            st.rerun()
    
    with control_col2:
        if st.button("🛑 Emergency Stop", use_container_width=True):
            st.session_state.system_running = False
            st.session_state.damper_forces = {
                damper: st.session_state.config_manager.DAMPER_FORCES.get('standby', 0) 
                if st.session_state.get('config_manager') 
                else 0 
                for damper in st.session_state.damper_forces.keys()
            }
            st.rerun()

    st.sidebar.markdown("---")
    
    # Simulation settings
    st.sidebar.subheader("⚙️ Simulation Settings")
    simulation_speed = st.sidebar.slider("Simulation Speed", 0.1, 2.0, 0.5, 0.1)
    max_cycles = st.sidebar.slider("Max Cycles", 50, 500, 200, 50)
    
    # System status display
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 System Status")
    status_indicator = st.sidebar.empty()
    cycle_display = st.sidebar.empty()
    performance_display = st.sidebar.empty()
    
    # Business intelligence section
    st.sidebar.markdown("---")
    st.sidebar.subheader("💼 Business Intelligence")
    
    if st.session_state.get('business_intel') and st.session_state.data_dict.get('risk_history'):
        try:
            efficiency, warning_ratio, critical_ratio = st.session_state.business_intel.calculate_operational_efficiency(
                st.session_state.data_dict['risk_history']
            )
            roi, cost_savings = st.session_state.business_intel.calculate_roi(
                st.session_state.performance_metrics.get('prevented_failures', 0),
                st.session_state.performance_metrics.get('cycles_completed', 0) / 10
            )
            
            st.sidebar.metric("Operational Efficiency", f"{efficiency:.1f}%")
            st.sidebar.metric("ROI", f"{roi:.0f}%")
            st.sidebar.metric("Cost Savings", f"${cost_savings:,.0f}")
            st.sidebar.metric("Prevented Failures", st.session_state.performance_metrics.get('prevented_failures', 0))
            
        except Exception as e:
            st.sidebar.warning(f"BI calculation error: {e}")

    # System architecture info
    st.sidebar.markdown("---")
    st.sidebar.subheader("🏗️ System Architecture")
    st.sidebar.write("• 4x Vibration Sensors")
    st.sidebar.write("• 4x Thermal Sensors")
    st.sidebar.write("• 1x Acoustic Sensor")
    st.sidebar.write("• 4x MR Dampers")
    st.sidebar.write("• AI: Enhanced Analytics")
    st.sidebar.write("• Safety: Real-time Monitoring")
    st.sidebar.write("• BI: ROI & Efficiency Tracking")

    # Main display area
    if not st.session_state.system_running:
        show_landing_page()
    else:
        # Run the enhanced monitoring loop
        run_enhanced_monitoring_loop(
            status_indicator, 
            cycle_display, 
            performance_display, 
            simulation_speed, 
            max_cycles
        )

    # Footer and system information
    st.markdown("---")
    
    # System logs and diagnostics (collapsible)
    with st.expander("🔧 System Diagnostics & Logs"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Performance Metrics")
            if st.session_state.performance_metrics:
                for metric, value in st.session_state.performance_metrics.items():
                    st.write(f"• {metric.replace('_', ' ').title()}: {value}")
        
        with col2:
            st.subheader("System Components")
            components_status = {
                "Config Manager": bool(st.session_state.get('config_manager')),
                "Data Manager": bool(st.session_state.get('data_manager')),
                "Safety Monitor": bool(st.session_state.get('safety_monitor')),
                "Business Intel": bool(st.session_state.get('business_intel')),
                "Enhanced AI": bool(st.session_state.get('enhanced_ai')),
                "Digital Twin": bool(st.session_state.get('digital_twin')),
                "Voice System": bool(st.session_state.get('voice_personality')),
                "Emotional Display": bool(st.session_state.get('emotional_display'))
            }
            
            for component, status in components_status.items():
                status_icon = "✅" if status else "❌"
                st.write(f"{status_icon} {component}")

        # Recent logs
        st.subheader("Recent System Logs")
        if st.session_state.system_logs:
            for i, log in enumerate(st.session_state.system_logs[-5:]):  # Show last 5 logs
                with st.expander(f"Log {i+1} - {log.get('timestamp', 'Unknown time')}"):
                    st.json(log)
        else:
            st.info("No system logs yet")

    # Final footer
    st.markdown("---")
    st.caption("""
    **AVCS DNA Matrix Soul v6.0** | Yeruslan Technologies | Predictive Maintenance System  
    *Enhanced with Safety Monitoring, Business Intelligence, and Advanced AI Analytics*
    """)

# Application entry point
if __name__ == "__main__":
    main()
