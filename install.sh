#!/bin/bash
# PWS Installation Script

set -e

echo "=== PWS Desktop Environment Installer ==="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt &> /dev/null; then
        DISTRO="debian"
    elif command -v dnf &> /dev/null; then
        DISTRO="fedora"
    elif command -v pacman &> /dev/null; then
        DISTRO="arch"
    else
        echo "Unsupported Linux distribution"
        exit 1
    fi
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Detected: $DISTRO"
echo ""

# Install dependencies
echo "Installing dependencies..."
case $DISTRO in
    debian)
        sudo apt update
        sudo apt install -y \
            python3 \
            python3-dev \
            python3-gi \
            gir1.2-gtk-4.0 \
            gir1.2-gdk-4.0 \
            libgtk-4-dev \
            libgdk-3-0 \
            firefox \
            gnome-terminal \
            gedit \
            nautilus \
            gnome-control-center
        ;;
    fedora)
        sudo dnf install -y \
            python3 \
            python3-devel \
            python3-gobject \
            gtk4-devel \
            firefox \
            gnome-terminal \
            gedit \
            nautilus \
            gnome-control-center
        ;;
    arch)
        sudo pacman -S --noconfirm \
            python \
            gobject-introspection \
            gtk4 \
            firefox \
            gnome-terminal \
            gedit \
            nautilus \
            gnome-control-center
        ;;
esac

echo ""
echo "Installing PWS..."

# Get installation directory
INSTALL_DIR="/opt/pws"
if [ ! -d "$INSTALL_DIR" ]; then
    sudo mkdir -p "$INSTALL_DIR"
fi

# Copy files
sudo cp pws_desktop.py "$INSTALL_DIR/"
sudo cp pws-session "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/pws-session"

# Install to PATH
sudo ln -sf "$INSTALL_DIR/pws-session" /usr/local/bin/pws-session
sudo chmod +x /usr/local/bin/pws-session

# Install desktop entry
sudo cp pws.desktop /usr/share/xsessions/
sudo cp pws.desktop /usr/share/wayland-sessions/

# Create config directory
mkdir -p ~/.config/pws

# Create default config
cat > ~/.config/pws/config.json << EOF
{
  "fullscreen": true,
  "theme": "dark",
  "accent_color": "#7dd3fc",
  "focus_rotation_interval": 5
}
EOF

echo ""
echo "=== Installation Complete ==="
echo ""
echo "PWS can now be selected as your desktop environment:"
echo "  1. Log out of your current session"
echo "  2. On the login screen, select 'PWS' from the session menu"
echo "  3. Log in with your credentials"
echo ""
echo "Or run directly with: pws-session"
echo ""
