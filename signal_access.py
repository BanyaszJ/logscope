"""
Signal access utility for providing dot notation access to MDF signals.
Creates a dynamic object that allows accessing signals like signal.car.tx
"""

import asammdf


class SignalAccessor:
    """
    Provides dot notation access to MDF signals.
    Usage: signal.car.tx to access signal named 'car.tx'
    """
    
    def __init__(self, mdf_file_path, file_id=None):
        self.mdf_file_path = mdf_file_path
        self.file_id = file_id
        self._mdf = None
        self._signal_cache = {}
        self._signal_names = []
        self._load_signal_names()
    
    def _load_signal_names(self):
        """Load available signal names from the MDF file."""
        try:
            mdf = self._get_mdf()
            
            # Extract all signal names
            signal_names = []
            
            # Method 1: Use list_channels() if available
            try:
                channels_info = mdf.list_channels()
                if channels_info:
                    signal_names = list(channels_info.keys())
            except AttributeError:
                pass
            
            # Method 2: Iterate through groups and channels
            if not signal_names:
                for group_idx, group in enumerate(mdf.groups):
                    for channel in group.channels:
                        if hasattr(channel, 'name') and channel.name:
                            signal_names.append(channel.name)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_signals = []
            for signal in signal_names:
                if signal and signal not in seen:
                    seen.add(signal)
                    unique_signals.append(signal)
            
            self._signal_names = unique_signals
            print(f"SignalAccessor: Loaded {len(self._signal_names)} signals")
            
        except Exception as e:
            print(f"Error loading signal names: {e}")
            self._signal_names = []
    
    def _get_mdf(self):
        """Get or create MDF object."""
        if self._mdf is None:
            self._mdf = asammdf.MDF(self.mdf_file_path)
        return self._mdf
    
    def __getattr__(self, name):
        """
        Handle dot notation access to signals.
        This method is called when accessing signal.something
        """
        # Handle nested access by building the full signal name
        return SignalBuilder(self, name)
    
    def __dir__(self):
        """Return available signal names for autocompletion."""
        # Return top-level signal components for tab completion
        components = set()
        for signal_name in self._signal_names:
            first_part = signal_name.split('.')[0]
            components.add(first_part)
        return list(components)
    
    def get_signal(self, signal_name):
        """
        Get signal data by name.
        Returns a list of values (samples from the signal).
        """
        if signal_name in self._signal_cache:
            return self._signal_cache[signal_name]
        
        try:
            mdf = self._get_mdf()
            signal_data = mdf.get(signal_name)
            
            if signal_data is None:
                raise ValueError(f"Signal '{signal_name}' not found")
            
            if len(signal_data.samples) == 0:
                raise ValueError(f"Signal '{signal_name}' has no data")
            
            # Convert to list for easy access
            signal_values = signal_data.samples.tolist()
            
            # Cache the result
            self._signal_cache[signal_name] = signal_values
            
            print(f"Loaded signal '{signal_name}': {len(signal_values)} samples")
            return signal_values
            
        except Exception as e:
            raise ValueError(f"Error loading signal '{signal_name}': {e}")
    
    def get_signal_with_time(self, signal_name):
        """
        Get signal data with timestamps.
        Returns a dict with 'time' and 'values' keys.
        """
        try:
            mdf = self._get_mdf()
            signal_data = mdf.get(signal_name)
            
            if signal_data is None:
                raise ValueError(f"Signal '{signal_name}' not found")
            
            if len(signal_data.samples) == 0:
                raise ValueError(f"Signal '{signal_name}' has no data")
            
            return {
                'time': signal_data.timestamps.tolist(),
                'values': signal_data.samples.tolist()
            }
            
        except Exception as e:
            raise ValueError(f"Error loading signal '{signal_name}': {e}")
    
    def list_signals(self):
        """Return list of all available signals."""
        return self._signal_names.copy()
    
    def search_signals(self, pattern):
        """Search for signals containing the given pattern."""
        pattern_lower = pattern.lower()
        return [name for name in self._signal_names if pattern_lower in name.lower()]
    
    def close(self):
        """Close the MDF file and clean up."""
        if self._mdf:
            try:
                self._mdf.close()
            except:
                pass
            self._mdf = None
        self._signal_cache.clear()


class SignalBuilder:
    """
    Helper class to build signal names through dot notation.
    Handles cases like signal.car.tx where 'car.tx' is the full signal name.
    """
    
    def __init__(self, accessor, name_parts):
        self.accessor = accessor
        if isinstance(name_parts, str):
            self.name_parts = [name_parts]
        else:
            self.name_parts = name_parts
    
    def __getattr__(self, name):
        """Continue building the signal name."""
        return SignalBuilder(self.accessor, self.name_parts + [name])
    
    def __repr__(self):
        """When accessed as a value, try to get the signal."""
        signal_name = '.'.join(self.name_parts)
        
        # Check if this exact signal name exists
        if signal_name in self.accessor._signal_names:
            try:
                return repr(self.accessor.get_signal(signal_name))
            except Exception as e:
                return f"<Error loading signal '{signal_name}': {e}>"
        
        # If not found, show available signals that start with this pattern
        matching = [name for name in self.accessor._signal_names 
                   if name.startswith(signal_name)]
        
        if matching:
            return f"<SignalBuilder '{signal_name}' - {len(matching)} matching signals: {matching[:5]}{'...' if len(matching) > 5 else ''}>"
        else:
            return f"<SignalBuilder '{signal_name}' - no matching signals found>"
    
    def __iter__(self):
        """Allow accessing the signal values directly."""
        signal_name = '.'.join(self.name_parts)
        return iter(self.accessor.get_signal(signal_name))
    
    def __len__(self):
        """Get length of signal data."""
        signal_name = '.'.join(self.name_parts)
        return len(self.accessor.get_signal(signal_name))
    
    def __getitem__(self, index):
        """Allow indexing into signal data."""
        signal_name = '.'.join(self.name_parts)
        return self.accessor.get_signal(signal_name)[index]
    
    def tolist(self):
        """Convert to list."""
        signal_name = '.'.join(self.name_parts)
        return self.accessor.get_signal(signal_name)
    
    def with_time(self):
        """Get signal data with timestamps."""
        signal_name = '.'.join(self.name_parts)
        return self.accessor.get_signal_with_time(signal_name)
    
    def __dir__(self):
        """Return available signal names for autocompletion."""
        current_name = '.'.join(self.name_parts)
        
        # Find signals that start with current name
        matching_signals = []
        for signal_name in self.accessor._signal_names:
            if signal_name.startswith(current_name + '.'):
                # Get the next part after current name
                remaining = signal_name[len(current_name) + 1:]
                next_part = remaining.split('.')[0]
                if next_part not in matching_signals:
                    matching_signals.append(next_part)
        
        return matching_signals


def create_signal_accessor(file_path, file_id=None):
    """Factory function to create a SignalAccessor instance."""
    return SignalAccessor(file_path, file_id)
