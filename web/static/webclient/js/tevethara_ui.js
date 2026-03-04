/**
 * Tevethara Custom UI JavaScript
 * Handles UI updates, state management, and UI mode toggling
 */

(function() {
    'use strict';

    // UI State object
    const TevetharaUI = {
        // Current UI mode ('dashboard' or 'compact')
        mode: 'dashboard',

        // HUD visibility ('collapsed' or 'expanded') — collapsed by default
        hudState: 'collapsed',

        // Initialize the custom UI
        init: function() {
            // Load saved preferences and apply before anything renders
            this.loadUIMode();
            this.loadHudState();

            // Set up toggle buttons
            this.setupUIToggle();
            this.setupHudToggle();

            // Set up message handlers for state updates from server
            this.setupMessageHandlers();

            // Apply initial mock data (will be replaced by server updates)
            this.applyMockData();
        },

        // Load UI mode from localStorage
        loadUIMode: function() {
            const savedMode = localStorage.getItem('tevethara_ui_mode');
            if (savedMode) {
                this.mode = savedMode;
                this.applyUIMode();
            }
        },

        // Save UI mode to localStorage
        saveUIMode: function() {
            localStorage.setItem('tevethara_ui_mode', this.mode);
        },

        // Apply current UI mode to body
        applyUIMode: function() {
            if (this.mode === 'compact') {
                document.body.classList.add('compact-mode');
            } else {
                document.body.classList.remove('compact-mode');
            }
        },

        // Set up UI toggle button click handler
        setupUIToggle: function() {
            const toggleBtn = document.getElementById('ui-mode-toggle');
            if (toggleBtn) {
                toggleBtn.addEventListener('click', () => {
                    this.mode = (this.mode === 'dashboard') ? 'compact' : 'dashboard';
                    this.applyUIMode();
                    this.saveUIMode();
                });
            }
        },

        // HUD collapse/expand
        loadHudState: function() {
            const saved = localStorage.getItem('tevethara_hud_state');
            // Default is 'collapsed'; only expand if explicitly saved as expanded
            this.hudState = (saved === 'expanded') ? 'expanded' : 'collapsed';
            this.applyHudState();
        },

        saveHudState: function() {
            localStorage.setItem('tevethara_hud_state', this.hudState);
        },

        applyHudState: function() {
            const container = document.getElementById('tevethara-container');
            if (!container) return;
            if (this.hudState === 'collapsed') {
                container.classList.add('hud-collapsed');
            } else {
                container.classList.remove('hud-collapsed');
            }
        },

        setupHudToggle: function() {
            const btn = document.getElementById('hud-toggle');
            if (btn) {
                btn.addEventListener('click', () => {
                    this.hudState = (this.hudState === 'collapsed') ? 'expanded' : 'collapsed';
                    this.applyHudState();
                    this.saveHudState();
                });
            }
        },

        // Set up handlers for OOB messages from the server.
        // Evennia emits a single "oob" event; our command name is nested inside.
        setupMessageHandlers: function() {
            const register = () => {
                if (typeof Evennia !== 'undefined' && Evennia.emitter) {
                    Evennia.emitter.on('oob', (args, kwargs) => {
                        if (!Array.isArray(args)) return;
                        args.forEach(cmdArr => {
                            if (!Array.isArray(cmdArr)) return;
                            const [cmd, , cmdKwargs] = cmdArr;
                            if (cmd === 'tev_map') {
                                const data = cmdKwargs && cmdKwargs.data
                                    ? cmdKwargs.data
                                    : '[ No map data ]';
                                TevetharaUI.updateMap(data);
                            }
                        });
                    });
                } else {
                    setTimeout(register, 200);
                }
            };
            register();
        },

        // Update room information in header
        updateRoom: function(data) {
            const roomName = document.getElementById('room-name');
            const exitsDisplay = document.getElementById('exits-display');

            if (data.name && roomName) {
                roomName.textContent = data.name;
            }

            if (data.exits && exitsDisplay) {
                const exitList = data.exits.join(' ');
                exitsDisplay.textContent = `[ Exits: ${exitList} ]`;
            }
        },

        // Update environment (weather, temp, time)
        updateEnvironment: function(data) {
            if (data.weather) {
                const weatherLabel = document.querySelector('.weather-label');
                const weatherIcon = document.querySelector('.weather-icon');
                if (weatherLabel) weatherLabel.textContent = data.weather.label || 'Clear';
                if (weatherIcon && data.weather.icon) weatherIcon.textContent = data.weather.icon;
            }

            if (data.temperature) {
                const tempDisplay = document.getElementById('temp-display');
                if (tempDisplay) tempDisplay.textContent = data.temperature;
            }

            if (data.time) {
                const timeDisplay = document.getElementById('time-display');
                if (timeDisplay) timeDisplay.textContent = data.time;
            }
        },

        // Update player vitals (HP, ST, MP)
        updateVitals: function(data) {
            if (data.hp !== undefined) {
                this.updateBar('hp', data.hp.current, data.hp.max);
            }

            if (data.stamina !== undefined) {
                this.updateBar('st', data.stamina.current, data.stamina.max);
            }

            if (data.mana !== undefined) {
                this.updateBar('mp', data.mana.current, data.mana.max);
            }
        },

        // Update XP progress
        updateXP: function(current, toNext) {
            this.updateBar('xp', current, toNext);
        },

        // Generic bar update helper
        updateBar: function(barId, current, max) {
            const barFill = document.getElementById(`${barId}-bar-fill`);
            const barText = document.getElementById(`${barId}-text`);

            if (barFill && barText) {
                const percentage = (current / max) * 100;
                barFill.style.width = percentage + '%';
                barText.textContent = `${current}/${max}`;
            }
        },

        // Update needs (hunger, thirst)
        updateNeeds: function(data) {
            if (data.hunger) {
                const hungerDisplay = document.getElementById('hunger-display');
                if (hungerDisplay) {
                    hungerDisplay.textContent = `🍖 ${data.hunger}`;
                }
            }

            if (data.thirst) {
                const thirstDisplay = document.getElementById('thirst-display');
                if (thirstDisplay) {
                    thirstDisplay.textContent = `💧 ${data.thirst}`;
                }
            }
        },

        // Update conditions ([Wet], [Poisoned], etc.)
        updateConditions: function(conditions) {
            const conditionsDisplay = document.getElementById('conditions-display');
            if (conditionsDisplay) {
                conditionsDisplay.innerHTML = '';

                conditions.forEach(condition => {
                    const tag = document.createElement('span');
                    tag.className = 'condition-tag';
                    tag.textContent = `[${condition}]`;
                    conditionsDisplay.appendChild(tag);
                });
            }
        },

        // Update the ASCII map display
        updateMap: function(asciiMap) {
            const content = document.getElementById('map-content');
            if (!content) return;
            content.innerHTML = '';
            const pre = document.createElement('pre');
            pre.style.margin = '0';
            pre.style.color = '#666';
            pre.style.fontSize = '11px';
            pre.style.lineHeight = '1.2';
            pre.textContent = asciiMap;
            content.appendChild(pre);
        },

        // Append a line to the world announcements panel
        appendWorldEvent: function(text) {
            const content = document.getElementById('world-content');
            if (!content) return;
            // Remove placeholder on first real event
            const placeholder = content.querySelector('.panel-placeholder');
            if (placeholder) placeholder.remove();

            const line = document.createElement('div');
            line.style.marginBottom = '2px';
            line.innerHTML = text;
            content.appendChild(line);
            // Auto-scroll to bottom
            content.scrollTop = content.scrollHeight;
        },

        // Update mob/encounter indicator
        updateMobIndicator: function(count) {
            const mobCount = document.getElementById('mob-count');
            const mobIndicator = document.querySelector('.mob-indicator');

            if (mobCount) {
                mobCount.textContent = count;
            }

            // Change styling based on threat level
            if (mobIndicator) {
                if (count > 0) {
                    mobIndicator.style.backgroundColor = '#3a1a1a';
                    mobIndicator.style.borderColor = '#884444';
                } else {
                    mobIndicator.style.backgroundColor = '#2a1a1a';
                    mobIndicator.style.borderColor = '#553333';
                }
            }
        },

        // Apply mock data for initial testing
        applyMockData: function() {
            console.log("Applying mock data for testing...");

            // This data is just for testing - will be replaced by server updates
            this.updateRoom({
                name: "The Wandering Path",
                exits: ["N", "S", "E", "W"]
            });

            this.updateEnvironment({
                weather: { icon: "☀️", label: "Clear" },
                temperature: "72°F",
                time: "Midday"
            });

            this.updateVitals({
                hp: { current: 85, max: 100 },
                stamina: { current: 60, max: 100 },
                mana: { current: 50, max: 50 }
            });

            this.updateXP(450, 1000);

            this.updateNeeds({
                hunger: "Satisfied",
                thirst: "Hydrated"
            });

            this.updateConditions([]);

            this.updateMobIndicator(0);
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            TevetharaUI.init();
            TevetharaInput.init();
        });
    } else {
        TevetharaUI.init();
        TevetharaInput.init();
    }

    // Expose TevetharaUI globally for server integration
    window.TevetharaUI = TevetharaUI;

})();

/**
 * Tevethara Input Enhancement
 * Adds better command history and input behavior
 */
(function() {
    'use strict';

    const TevetharaInput = {
        commandHistory: [],
        historyIndex: -1,
        maxHistory: 50,

        init: function() {
            console.log("Tevethara Input initializing...");

            // Load history from localStorage
            this.loadHistory();

            // Set up input field keydown handler
            this.setupInputHandler();

            console.log("Tevethara Input initialized!");
        },

        loadHistory: function() {
            const saved = localStorage.getItem('tevethara_command_history');
            if (saved) {
                try {
                    this.commandHistory = JSON.parse(saved);
                } catch(e) {
                    console.log("Could not load command history");
                }
            }
        },

        saveHistory: function() {
            // Keep only last maxHistory items
            if (this.commandHistory.length > this.maxHistory) {
                this.commandHistory = this.commandHistory.slice(-this.maxHistory);
            }
            localStorage.setItem('tevethara_command_history', JSON.stringify(this.commandHistory));
        },

        addToHistory: function(command) {
            if (!command || command.trim() === '') return;

            // Don't add duplicates of the last command
            if (this.commandHistory.length > 0 &&
                this.commandHistory[this.commandHistory.length - 1] === command) {
                return;
            }

            this.commandHistory.push(command);
            this.saveHistory();
            this.historyIndex = -1; // Reset to end
        },

        setupInputHandler: function() {
            const inputField = document.getElementById('inputfield');
            if (!inputField) {
                console.log("Input field not found, retrying in 100ms...");
                setTimeout(() => this.setupInputHandler(), 100);
                return;
            }

            // Intercept keydown events BEFORE Evennia's handler
            inputField.addEventListener('keydown', (event) => {
                // Up arrow (without Shift)
                if (event.keyCode === 38 && !event.shiftKey) {
                    event.preventDefault();
                    this.navigateHistory('up', inputField);
                    return false;
                }

                // Down arrow (without Shift)
                if (event.keyCode === 40 && !event.shiftKey) {
                    event.preventDefault();
                    this.navigateHistory('down', inputField);
                    return false;
                }

                // Enter key - save to history
                if (event.keyCode === 13 && !event.shiftKey) {
                    const command = inputField.value.trim();
                    if (command) {
                        this.addToHistory(command);
                    }
                }
            }, true); // Use capture phase to run before other handlers

            console.log("Input handler attached to #inputfield");
        },

        navigateHistory: function(direction, inputField) {
            if (this.commandHistory.length === 0) return;

            if (direction === 'up') {
                // Move backwards in history (older commands)
                if (this.historyIndex < this.commandHistory.length - 1) {
                    this.historyIndex++;
                }
            } else if (direction === 'down') {
                // Move forwards in history (newer commands)
                if (this.historyIndex > -1) {
                    this.historyIndex--;
                }
            }

            // Set input field value
            if (this.historyIndex === -1) {
                inputField.value = ''; // At the end, clear input
            } else {
                const historyCommand = this.commandHistory[this.commandHistory.length - 1 - this.historyIndex];
                inputField.value = historyCommand;
            }

            // Move cursor to end
            inputField.setSelectionRange(inputField.value.length, inputField.value.length);
        }
    };

    // Expose globally
    window.TevetharaInput = TevetharaInput;

})();
