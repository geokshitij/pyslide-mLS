# Contributing to pyslide-mLS

Thank you for your interest in contributing to pyslide-mLS! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/geokshitij/pyslide-mLS/issues) section
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem or suggestion
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Python version, OS, and relevant environment details

### Submitting Changes

1. **Fork the Repository**
   ```bash
   git clone https://github.com/geokshitij/pyslide-mLS.git
   cd pyslide-mLS
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add comments where necessary
   - Update documentation if needed

4. **Test Your Changes**
   ```bash
   python tests/test_installation.py
   python tests/test_matlab_comparison.py
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add descriptive commit message"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Provide a clear description of your changes

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Testing

- Ensure all existing tests pass
- Add tests for new features
- Verify MATLAB-Python compatibility for core calculations

### Documentation

- Update README.md if adding new features
- Add inline comments for complex logic
- Update docstrings if changing function behavior

## Areas for Contribution

- **Bug Fixes**: Fix any reported issues
- **Performance**: Optimize calculations or data handling
- **Features**: Add new analysis tools or visualizations
- **Documentation**: Improve guides, examples, or comments
- **Testing**: Add more test cases or improve test coverage
- **UI/UX**: Enhance the web interface

## Questions?

Feel free to open an issue for discussion before starting work on major changes.

Thank you for contributing! 🙏
