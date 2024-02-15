#SBATCH --job-name=SlurmTest
#SBATCH --mail-user=clhaynes@umich.edu
#SBATCH --mail-type=BEGIN,END
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=1000m 
#SBATCH --time=00-00:01:00
#SBATCH --account=zamanlh0
#SBATCH --partition=standard
#SBATCH --output=/home/%u/%x-%j.log

USERNAME=clhaynes
EXPERIMENT_ID=2024-2-15-HPCCTest
OUTPUT_DIR=/scratch/zamanlh_root/zamanlh0/${USERNAME}/SlurmTest
CONFIG_DIR=/home/${USERNAME}/Documents/AvidaPhageCoevSimulations/experiments/${EXPERIMENT_ID}/config


RUN_DIR=${OUTPUT_DIR}

mkdir -p ${RUN_DIR}

cd ${CONFIG_DIR}
cp * ${RUN_DIR}
cd ${RUN_DIR}

echo "$PWD" >> log.txt