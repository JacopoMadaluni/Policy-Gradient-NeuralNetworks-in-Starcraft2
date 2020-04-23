Since some of the checkpoints were created using previous versions of the software, It might not be possible to load some of the networks.
If, while loading a checkpoint the following error occurs:
"ValueError: Cannot feed value of shape (...) for Tensor 'parameters/input:0', which has shape '(...)'"
this means the checkpoint is of an older version and cannot be loaded.
This might happen for older networks smaller than 128x128.