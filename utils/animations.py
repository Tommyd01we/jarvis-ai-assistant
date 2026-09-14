import time
import sys
import threading
from typing import List, Dict, Any, Optional
from utils.logger import Logger

class AnimationFrame:
    """Represents a single animation frame"""
    
    def __init__(self, content: str, duration: float = 0.1):
        self.content = content
        self.duration = duration


class PanelAnimation:
    """Base class for panel animations"""
    
    def __init__(self, width: int = 60, height: int = 10):
        self.width = width
        self.height = height
        self.logger = Logger()
        self.is_running = False
        self.animation_thread = None
    
    def render(self) -> str:
        """Render the current frame"""
        raise NotImplementedError
    
    def start(self, duration: float = 2.0):
        """Start animation"""
        self.is_running = True
        start_time = time.time()
        
        while self.is_running and (time.time() - start_time) < duration:
            frame = self.render()
            self._clear_screen()
            print(frame)
            time.sleep(0.05)
    
    def stop(self):
        """Stop animation"""
        self.is_running = False
    
    def _clear_screen(self):
        """Clear terminal screen"""
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()


class LoadingAnimation(PanelAnimation):
    """Loading spinner animation"""
    
    def __init__(self, text: str = "Processing", width: int = 60):
        super().__init__(width, 3)
        self.text = text
        self.spinner_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.frame_index = 0
    
    def render(self) -> str:
        """Render loading spinner"""
        spinner = self.spinner_frames[self.frame_index % len(self.spinner_frames)]
        self.frame_index += 1
        
        frame = f"""
╔{'═' * (self.width - 2)}╗
║ {spinner} {self.text:<{self.width - 5}} ║
╚{'═' * (self.width - 2)}╝
"""
        return frame


class TypingAnimation(PanelAnimation):
    """Typing effect animation"""
    
    def __init__(self, text: str, width: int = 60):
        super().__init__(width, 5)
        self.text = text
        self.current_index = 0
    
    def render(self) -> str:
        """Render typing effect"""
        displayed_text = self.text[:self.current_index]
        cursor = '▌' if self.current_index < len(self.text) else ' '
        
        self.current_index = min(self.current_index + 1, len(self.text))
        
        # Wrap text to width
        lines = self._wrap_text(displayed_text + cursor, self.width - 4)
        
        frame = f"""
╔{'═' * (self.width - 2)}╗
║                                                            ║
"""
        for line in lines:
            frame += f"║ {line:<{self.width - 4}} ║\n"
        
        frame += f"╚{'═' * (self.width - 2)}╝"
        return frame
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to specified width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines


class ScanlineAnimation(PanelAnimation):
    """Scanline effect animation"""
    
    def __init__(self, width: int = 60, height: int = 8):
        super().__init__(width, height)
        self.scanline_pos = 0
    
    def render(self) -> str:
        """Render scanline animation"""
        frame = f"╔{'═' * (self.width - 2)}╗\n"
        
        for i in range(self.height - 2):
            if i == self.scanline_pos % (self.height - 2):
                frame += f"║{'─' * (self.width - 2)}║\n"
            else:
                frame += f"║{' ' * (self.width - 2)}║\n"
        
        frame += f"╚{'═' * (self.width - 2)}╝"
        self.scanline_pos += 1
        
        return frame


class ProgressBarAnimation(PanelAnimation):
    """Progress bar animation"""
    
    def __init__(self, total: int = 100, width: int = 60):
        super().__init__(width, 5)
        self.total = total
        self.current = 0
    
    def update(self, current: int):
        """Update progress"""
        self.current = min(current, self.total)
    
    def render(self) -> str:
        """Render progress bar"""
        bar_width = self.width - 10
        filled = int((self.current / self.total) * bar_width)
        empty = bar_width - filled
        
        percentage = int((self.current / self.total) * 100)
        
        frame = f"""
╔{'═' * (self.width - 2)}╗
║ Processing: [{('█' * filled)}{('░' * empty)}] {percentage}% ║
╚{'═' * (self.width - 2)}╝
"""
        return frame


class PulseAnimation(PanelAnimation):
    """Pulsing glow effect animation"""
    
    def __init__(self, text: str = "Jarvis", width: int = 60):
        super().__init__(width, 5)
        self.text = text
        self.intensity = 0
        self.direction = 1
    
    def render(self) -> str:
        """Render pulse effect"""
        # Update intensity
        self.intensity += self.direction * 0.1
        if self.intensity >= 1.0:
            self.direction = -1
        elif self.intensity <= 0.0:
            self.direction = 1
        
        # Create glow effect
        glow_chars = ['·', '○', '◎', '●']
        glow_index = int(self.intensity * (len(glow_chars) - 1))
        glow = glow_chars[glow_index]
        
        padding = (self.width - len(self.text) - 2) // 2
        
        frame = f"""
╔{'═' * (self.width - 2)}╗
║{' ' * padding}{glow} {self.text} {glow}{' ' * (self.width - len(self.text) - padding - 6)}║
╚{'═' * (self.width - 2)}╝
"""
        return frame


class WaveAnimation(PanelAnimation):
    """Wave effect animation"""
    
    def __init__(self, width: int = 60, height: int = 8):
        super().__init__(width, height)
        self.wave_offset = 0
    
    def render(self) -> str:
        """Render wave effect"""
        import math
        
        frame = f"╔{'═' * (self.width - 2)}╗\n"
        
        for row in range(self.height - 2):
            line = ""
            for col in range(self.width - 2):
                # Calculate wave position
                wave_val = math.sin((col + self.wave_offset) / 5 + row / 3) * 0.5 + 0.5
                char = '█' if wave_val > 0.5 else '░'
                line += char
            
            frame += f"║{line}║\n"
        
        frame += f"╚{'═' * (self.width - 2)}╝"
        self.wave_offset += 1
        
        return frame


class MatrixRainAnimation(PanelAnimation):
    """Matrix-style rain effect"""
    
    def __init__(self, width: int = 60, height: int = 10):
        super().__init__(width, height)
        self.columns = [0] * (width - 2)
        self.chars = '░▒▓█'
    
    def render(self) -> str:
        """Render matrix rain"""
        import random
        
        frame = f"╔{'═' * (self.width - 2)}╗\n"
        
        # Update columns
        for i in range(len(self.columns)):
            self.columns[i] = (self.columns[i] + 1) % (self.height - 2)
        
        # Render each row
        for row in range(self.height - 2):
            line = ""
            for col in range(self.width - 2):
                if self.columns[col] == row:
                    char = self.chars[random.randint(0, len(self.chars) - 1)]
                    line += char
                else:
                    line += ' '
            
            frame += f"║{line}║\n"
        
        frame += f"╚{'═' * (self.width - 2)}╝"
        return frame


class JarvisInitializationAnimation(PanelAnimation):
    """Jarvis startup animation sequence"""
    
    def __init__(self, width: int = 60):
        super().__init__(width, 10)
        self.stage = 0
        self.substage = 0
    
    def render(self) -> str:
        """Render initialization sequence"""
        frame = f"""
╔{'═' * (self.width - 2)}╗
║{' ' * (self.width - 2)}║
║{'JARVIS AI ENGINE INITIALIZATION'.center(self.width - 2)}║
║{' ' * (self.width - 2)}║
"""
        
        stages = [
            "⟳ Initializing Core Systems...",
            "✓ Core Systems Ready",
            "⟳ Loading NLP Processor...",
            "✓ NLP Processor Loaded",
            "⟳ Initializing Memory Manager...",
            "✓ Memory Manager Ready",
            "⟳ Starting AI Models...",
            "✓ All Systems Online",
            "✓ Jarvis Ready for Interaction"
        ]
        
        for i, stage in enumerate(stages):
            if i < self.stage:
                frame += f"║ ✓ {stages[i][4:] if '✓' in stages[i] else stages[i][2:]:<{self.width - 6}}║\n"
            elif i == self.stage:
                frame += f"║ {stage:<{self.width - 4}}║\n"
            else:
                frame += f"║{' ' * (self.width - 2)}║\n"
        
        frame += f"╚{'═' * (self.width - 2)}╝"
        
        self.substage += 1
        if self.substage >= 3:
            self.substage = 0
            self.stage = min(self.stage + 1, len(stages) - 1)
        
        return frame


class AnimationManager:
    """Manages various animations throughout the application"""
    
    def __init__(self):
        self.logger = Logger()
        self.current_animation: Optional[PanelAnimation] = None
        self.animation_thread: Optional[threading.Thread] = None
    
    def show_loading(self, text: str = "Processing", duration: float = 2.0):
        """Show loading animation"""
        animation = LoadingAnimation(text)
        self._run_animation(animation, duration)
    
    def show_typing(self, text: str, duration: float = None):
        """Show typing animation"""
        animation = TypingAnimation(text)
        if duration is None:
            duration = len(text) / 10  # Estimate based on text length
        self._run_animation(animation, duration)
    
    def show_scanlines(self, duration: float = 2.0):
        """Show scanline animation"""
        animation = ScanlineAnimation()
        self._run_animation(animation, duration)
    
    def show_progress(self, total: int = 100, duration: float = 3.0):
        """Show progress bar animation"""
        animation = ProgressBarAnimation(total)
        self._run_animation(animation, duration)
    
    def show_pulse(self, text: str = "Jarvis", duration: float = 2.0):
        """Show pulse animation"""
        animation = PulseAnimation(text)
        self._run_animation(animation, duration)
    
    def show_wave(self, duration: float = 3.0):
        """Show wave animation"""
        animation = WaveAnimation()
        self._run_animation(animation, duration)
    
    def show_matrix_rain(self, duration: float = 3.0):
        """Show matrix rain animation"""
        animation = MatrixRainAnimation()
        self._run_animation(animation, duration)
    
    def show_initialization(self):
        """Show Jarvis initialization sequence"""
        animation = JarvisInitializationAnimation()
        self._run_animation(animation, 30.0)
    
    def _run_animation(self, animation: PanelAnimation, duration: float):
        """Run animation in main thread"""
        try:
            animation.start(duration)
        except Exception as e:
            self.logger.error(f"Animation error: {str(e)}")
    
    def stop_animation(self):
        """Stop current animation"""
        if self.current_animation:
            self.current_animation.stop()
