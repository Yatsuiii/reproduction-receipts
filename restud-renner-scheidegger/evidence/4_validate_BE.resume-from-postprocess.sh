#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate rep
N_PROCS=4
cd dptorch
parallel -j $N_PROCS :::: post_processing_commands.txt 



cd ../figure_replication
NOTEBOOKS=(
    "Sec_5_overreporting/2D_simulation_and_error.ipynb"
    "Sec_5_overreporting/4D_simulation_and_error.ipynb"
)

for nb in "${NOTEBOOKS[@]}"; do
    echo "Executing $nb..."
    
    jupyter nbconvert --to notebook --execute --inplace "$nb"
    
    if [ $? -ne 0 ]; then
        echo "Error encountered while executing $nb. Stopping the sequence."
        exit 1
    fi
    
    echo "Successfully finished $nb"
    echo "-----------------------------------"
done

echo "All notebooks executed successfully!"

NOTEBOOKS=(
    "Sec_4_5_Fernandes_Phelan/Table_10D_fernandes_phelan.ipynb"
    "Sec_5_overreporting/Plot_Table_2D_overreporting.ipynb"
    "Sec_5_overreporting/Plot_Table_4D_overreporting.ipynb"
)

for nb in "${NOTEBOOKS[@]}"; do
    echo "Executing $nb..."

    jupyter nbconvert --to notebook --execute --inplace "$nb"

    if [ $? -ne 0 ]; then
        echo "Error encountered while executing $nb. Stopping."
        exit 1
    fi

    echo "Successfully finished $nb"
    echo "-----------------------------------"
done

echo "All scripts and notebooks executed successfully!"

OUTPUT_DIR="figure_and_table_outputs"

rm -rf "$OUTPUT_DIR/4"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/4"

mv Sec_4_5_Fernandes_Phelan/*.pdf "$OUTPUT_DIR/4/"
mv Sec_4_5_Fernandes_Phelan/*.tex "$OUTPUT_DIR/4/"
mv Sec_5_overreporting/*.pdf "$OUTPUT_DIR/4/"
mv Sec_5_overreporting/*.tex "$OUTPUT_DIR/4/"
