#!/bin/bash

echo "=============================================="
echo "== Starting Training Environment...        =="
echo "=============================================="
echo

cd ..

echo "-> Activating Training Environment..."
source venv_training/bin/activate
cd training
echo "Training environment ready. Run 'python train_segmentation.py' to start training."
exec $SHELL
