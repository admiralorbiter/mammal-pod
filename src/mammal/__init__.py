"""Project MAMMAL: Metacognitive Assessment & Machine Modeling of an Adaptive Learner."""

try:
    import six
    if hasattr(six, "_SixMetaPathImporter") and not hasattr(six._SixMetaPathImporter, "_path"):
        six._SixMetaPathImporter._path = None
except ImportError:
    pass

__version__ = "0.1.0"
