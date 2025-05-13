import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
#import numpy as np
#import cv2
#from skimage.color import rgb2gray
#from skimage import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from logic import CurrencyDetector

# Modern Color Scheme
MAIN_BG = '#1b263b'  # Dark blue background
PRIMARY_COLOR = '#2B3A67'  # Navy blue
SECONDARY_COLOR = '#E84545'  # Vibrant red
ACCENT_COLOR = '#53354A'  # Deep purple  
TEXT_COLOR = '#FFFFFF'  # White text   
BUTTON_BG = '#E84545'  # Red buttons      
HOVER_COLOR = '#FF6B6B'  # Lighter red for hover  
FRAME_BG = '#2B3A67'  # Navy blue for frames     

# Paths to images
LOGO_PATH = r"gui\detective.png"
MODEL_PATH = r"model.joblib"

class ModernFrame(tk.Frame):
    """Custom frame without visible borders for clean modern styling"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            bg=kwargs.get('bg', FRAME_BG),
            highlightthickness=0,  # Remove border
            bd=0  # Remove border
        )

class ModernButton(tk.Button):
    """Custom button class with modern styling and hover effects"""
    def __init__(self, master, text, command, width=20, height=40, font_size=11, is_main=False):
        self.default_bg = BUTTON_BG
        self.hover_bg = HOVER_COLOR
        
        # Adjust size and style for main button
        if is_main:
            font_size = 14
            width = 25
        
        super().__init__(
            master,
            text=text,
            command=command,
            bg=self.default_bg,
            fg=TEXT_COLOR,
            font=("Helvetica", font_size, "bold"),
            bd=0,
            relief="flat",
            activebackground=self.hover_bg,
            activeforeground=TEXT_COLOR,
            cursor="hand2",
            width=width,
            padx=25,
            pady=12 if is_main else 8,
            highlightthickness=0,
            compound="center"
        )
        
        # Create canvas for rounded button    
        self.canvas = tk.Canvas(            
            master,
            width=self.winfo_reqwidth(),         
            height=self.winfo_reqheight(),           
            bg=MAIN_BG,
            highlightthickness=0                          
        )
        
        # Bind hover events                                
        self.bind("<Enter>", self.on_enter)                        
        self.bind("<Leave>", self.on_leave)                         
        
    def on_enter(self, e):
        """Mouse enter effect"""
        self.configure(background=self.hover_bg)
        # Smooth transition effect
        for i in range(5):
            self.update_idletasks()
            self.after(20)
        
    def on_leave(self, e):                            
        """Mouse leave effect"""                              
        self.configure(background=self.default_bg)                      
        # Smooth transition effect                        
        for i in range(5):                    
            self.update_idletasks()                        
            self.after(20)                      

class ActionText(tk.Label):          
    """Clickable text with hover effect"""            
    def __init__(self, master, text, command, **kwargs):
        super().__init__(         
            master,              
            text=text,                    
            font=("Helvetica", 12),                    
            bg=MAIN_BG,                     
            fg=TEXT_COLOR,                    
            cursor="hand2",              
            **kwargs                      
        )                          
        self.command = command                
        self.bind("<Enter>", self.on_enter)                 
        self.bind("<Leave>", self.on_leave)           
        self.bind("<Button-1>", self.on_click)                     
        
    def on_enter(self, e):                        
        self.configure(fg=SECONDARY_COLOR)               
        
    def on_leave(self, e):                         
        self.configure(fg=TEXT_COLOR)                 
        
    def on_click(self, e):                
        self.command()                         

class FakeMoneyDetective:                        
    def __init__(self, root):                
        self.root = root                    
        self.root.title("Fake Money Detective")              
        self.root.geometry("1200x900")           
        self.root.configure(bg=MAIN_BG)        
        
        # Initialize the detector                                
        self.detector = CurrencyDetector(MODEL_PATH)                  
        if self.detector.model is None:                       
            messagebox.showerror("Error", "Could not load model")                        
            
        self.current_image_path = None                          
        self.setup_ui()                                      
        
    def setup_ui(self):               
        # Main container                    
        self.main_container = ModernFrame(self.root, bg=MAIN_BG)                 
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)           
        
        # Header section with logo and title                   
        header = ModernFrame(self.main_container, bg=MAIN_BG)                           
        header.pack(fill=tk.X, pady=(0, 30))                                            
        
        try:
            logo_img = Image.open(LOGO_PATH)
            logo_img = logo_img.resize((130, 130), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            tk.Label(
                header,
                image=self.logo_photo,
                bg=MAIN_BG
            ).pack(side=tk.LEFT, padx=(50, 20))
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        title_frame = ModernFrame(header, bg=MAIN_BG)
        title_frame.pack(side=tk.LEFT, pady=20)
        
        tk.Label(
            title_frame,
            text="Currency",
            font=("Helvetica", 36, "bold"),
            bg=MAIN_BG,
            fg=TEXT_COLOR
        ).pack(anchor="w")
        
        tk.Label(
            title_frame,
            text="Authentication System",
            font=("Helvetica", 24),
            bg=MAIN_BG,
            fg=SECONDARY_COLOR
        ).pack(anchor="w")
        
        # Content section
        content = ModernFrame(self.main_container, bg=MAIN_BG)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Image frames container
        images_frame = ModernFrame(content, bg=MAIN_BG)
        images_frame.pack(fill=tk.X, padx=50, pady=20)
        
        # Original image container
        original_container = ModernFrame(images_frame, bg=FRAME_BG)
        original_container.pack(side=tk.LEFT, expand=True, padx=10)
        
        tk.Label(
            original_container,
            text="Original Image",
            font=("Helvetica", 14, "bold"),
            bg=FRAME_BG,
            fg=TEXT_COLOR
        ).pack(pady=10)
        
        self.image_frame = ModernFrame(
            original_container,
            bg=FRAME_BG,
            width=300,
            height=200
        )
        self.image_frame.pack(padx=20, pady=10)
        self.image_frame.pack_propagate(False)
        
        self.image_label = tk.Label(
            self.image_frame,
            bg=FRAME_BG
        )
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Processed image container
        processed_container = ModernFrame(images_frame, bg=FRAME_BG)
        processed_container.pack(side=tk.LEFT, expand=True, padx=10)
        
        tk.Label(
            processed_container,
            text="Edge Detection",
            font=("Helvetica", 14, "bold"),
            bg=FRAME_BG,
            fg=TEXT_COLOR
        ).pack(pady=10)
        
        self.processed_frame = ModernFrame(
            processed_container,
            bg=FRAME_BG,
            width=300,
            height=200
        )
        self.processed_frame.pack(padx=20, pady=10)
        self.processed_frame.pack_propagate(False)
        
        self.processed_label = tk.Label(           
            self.processed_frame,              
            bg=FRAME_BG                     
        )                                                  
        self.processed_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Results section
        results_frame = ModernFrame(content, bg=MAIN_BG)
        results_frame.pack(fill=tk.X, pady=20)
        
        self.result_label = tk.Label(
            results_frame,
            text="Upload an image to detect",
            font=("Helvetica", 20, "bold"),
            bg=MAIN_BG,
            fg=TEXT_COLOR
        )
        self.result_label.pack()
        
        self.confidence_label = tk.Label(
            results_frame,
            text="",
            font=("Helvetica", 16),
            bg=MAIN_BG,
            fg=TEXT_COLOR
        )
        self.confidence_label.pack(pady=5)
        
        # Main button and actions section
        actions_frame = ModernFrame(content, bg=MAIN_BG)
        actions_frame.pack(pady=30)
        
        self.main_button = ModernButton(
            actions_frame,
            text="Upload Image",
            command=self.upload_currency,
            is_main=True
        )
        self.main_button.pack(pady=(0, 20))
        
        # Action texts
        actions_text_frame = ModernFrame(actions_frame, bg=MAIN_BG)
        actions_text_frame.pack()
        
        ActionText(
            actions_text_frame,
            text="Analyze Features",
            command=self.show_analysis
        ).pack(pady=5)
        
        ActionText(
            actions_text_frame,
            text="Meet the Team",
            command=self.show_developers
        ).pack(pady=5)

    def show_developers(self):
        if hasattr(self, 'dev_window') and self.dev_window.winfo_exists():
            self.dev_window.lift()
            return
            
        self.dev_window = tk.Toplevel(self.root)
        self.dev_window.title("Development Team")
        self.dev_window.geometry("400x400")
        self.dev_window.configure(bg=MAIN_BG)
        self.dev_window.transient(self.root)
        
        dev_frame = ModernFrame(self.dev_window, bg=FRAME_BG)
        dev_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            dev_frame,
            text="Development Team",
            font=("Helvetica", 24, "bold"),
            bg=FRAME_BG,
            fg=TEXT_COLOR
        ).pack(pady=20)
        
        developers = [
            "Abdulrahman Mohamed",
            "Abdulrahman Nasser",
            "Amr Khaled El Sayed",
            "Abdulrahman Fawzi"
        ]
        
        for dev in developers:
            tk.Label(
                dev_frame,
                text=dev,
                font=("Helvetica", 14),
                bg=FRAME_BG,
                fg=TEXT_COLOR
            ).pack(pady=10)
            
        # Close button with better styling
        button_frame = ModernFrame(dev_frame, bg=FRAME_BG)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        ModernButton(
            button_frame,
            text="Close",
            command=self.dev_window.destroy,
            width=10,
            font_size=11
        ).pack(pady=10)

    def show_analysis(self):
        if not self.current_image_path:
            return
            
        if hasattr(self, 'analysis_window') and self.analysis_window.winfo_exists():
            self.analysis_window.lift()
            return
            
        self.analysis_window = tk.Toplevel(self.root)
        self.analysis_window.title("Feature Analysis")
        self.analysis_window.geometry("800x600")
        self.analysis_window.configure(bg=MAIN_BG)
        self.analysis_window.transient(self.root)
        
        analysis_frame = ModernFrame(self.analysis_window, bg=MAIN_BG)
        analysis_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        try:
            _, _, features = self.detector.predict_banknote(self.current_image_path)
            
            tk.Label(
                analysis_frame,
                text="Feature Analysis",
                font=("Helvetica", 24, "bold"),
                bg=MAIN_BG,
                fg=TEXT_COLOR
            ).pack(pady=(0, 30))
            
            # Create modern styled chart
            fig = plt.Figure(figsize=(10, 6), dpi=100)
            fig.patch.set_facecolor(MAIN_BG)
            
            ax = fig.add_subplot(111)
            feature_names = ['Variance', 'Skewness', 'Kurtosis', 'Entropy']
            bars = ax.bar(feature_names, features, color=SECONDARY_COLOR)
            
            # Style the plot
            ax.set_facecolor(MAIN_BG)
            ax.tick_params(colors=TEXT_COLOR, labelsize=12)
            for spine in ax.spines.values():
                spine.set_color(TEXT_COLOR)
            
            # Add value labels
            for bar, val in zip(bars, features):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{val:.4f}',
                    ha='center',
                    va='bottom',
                    color=TEXT_COLOR,
                    fontsize=10
                )
            
            canvas = FigureCanvasTkAgg(fig, master=analysis_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)
            
            # Add explanation
            explanation = tk.Label(
                analysis_frame,
                text="These features are extracted using Sobel edge detection\n"
                     "and are used by the model to determine authenticity.",
                font=("Helvetica", 12),
                bg=MAIN_BG,
                fg=TEXT_COLOR,
                justify=tk.CENTER
            )
            explanation.pack(pady=20)
            
        except Exception as e:
            tk.Label(
                analysis_frame,
                text=f"Error analyzing features: {e}",
                font=("Helvetica", 12),
                bg=MAIN_BG,
                fg=TEXT_COLOR
            ).pack(pady=20)
            
        ModernButton(
            analysis_frame,
            text="Close",
            command=self.analysis_window.destroy,
            width=10,
            font_size=10
        ).pack(pady=20)

    def upload_currency(self):
        """Handle currency image upload and processing"""
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        path = filedialog.askopenfilename(title="Select Currency Image", filetypes=filetypes)
        if not path:
            return
            
        self.current_image_path = path
        
        try:
            # Display original image
            img = Image.open(path)
            img.thumbnail((280, 180), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            
            # Process and display edge detection
            grad_norm = self.detector.process_image(path)
            processed_img = Image.fromarray(grad_norm)
            processed_img.thumbnail((280, 180), Image.Resampling.LANCZOS)
            processed_photo = ImageTk.PhotoImage(processed_img)
            self.processed_label.config(image=processed_photo)
            self.processed_label.image = processed_photo
            
            if self.detector.model is not None:
                result, confidence, _ = self.detector.predict_banknote(path)
                
                if result and "REAL" in result:
                    self.result_label.config(text=result, fg='#4CAF50')
                else:
                    self.result_label.config(text=result, fg=SECONDARY_COLOR)
                
                if confidence is not None:
                    self.confidence_label.config(
                        text=f"Confidence: {confidence:.2f}%",
                        fg=TEXT_COLOR
                    )
                
            else:
                self.result_label.config(text="Model not loaded", fg=TEXT_COLOR)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {e}")
            self.result_label.config(text="Analysis Error", fg=TEXT_COLOR)
            self.confidence_label.config(text="")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = FakeMoneyDetective(root)
    root.mainloop()
