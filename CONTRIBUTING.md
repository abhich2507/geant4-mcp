# Contributing to GEANT4 MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/<your-username>/geant4-mcp.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## Development Setup

### Prerequisites
- Docker Desktop installed
- Git
- Text editor or IDE

### Building
```bash
docker-compose build
docker-compose up -d
```

### Testing Changes

After modifying code:
```bash
# Rebuild and restart container
docker-compose restart

# Check logs
docker logs geant4-simulation

# Test simulation
docker exec geant4-simulation python3 simulation.py
```

## Code Style

### Python
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Comments
- Explain WHY, not WHAT
- Use comments for complex physics calculations
- Document GEANT4-specific concepts

## Types of Contributions

### Bug Reports
When reporting bugs, include:
- Your platform (macOS, Windows, Linux)
- Docker version
- Steps to reproduce
- Error messages and logs
- Expected vs actual behavior

### Feature Requests
- Describe the use case
- Explain why it would be useful
- Consider implementation complexity

### Code Contributions

**Simulation Features**:
- New particle types
- Additional detector geometries
- Physics list options
- Output formats

**MCP Server Features**:
- New tools/commands
- Better error handling
- Performance improvements

**Documentation**:
- Clarify setup instructions
- Add examples
- Fix typos
- Improve troubleshooting

## Pull Request Process

1. **Update documentation** if needed
2. **Test on your platform**
3. **Describe your changes** clearly in the PR
4. **Link related issues** if applicable
5. **Be responsive** to feedback

## Testing Checklist

Before submitting a PR, verify:

- [ ] Docker container builds successfully
- [ ] Simulation runs without errors
- [ ] MCP server connects to Claude Desktop
- [ ] No Python syntax errors
- [ ] Documentation is updated
- [ ] .gitignore is appropriate
- [ ] No sensitive data committed

## Questions?

Open an issue with the `question` label!

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
