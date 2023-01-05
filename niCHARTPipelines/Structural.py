from nipype import Node, Workflow

import DeepMRSegInterface
import MaskImageInterface

# Create DLICV Node
dlicv = Node(DeepMRSegInterface.DeepMRSegInference(), name='dlicv')
dlicv.inputs.in_file = '/nichart/data/F1/2.16.840.1.114362.1.12066432.24920037488.604832115.605.168.nii.gz'
dlicv.inputs.mdl_dir1 = '/nichart/models/DLICV/LPS'
dlicv.inputs.out_file = '/nichart/data/F1/dlicv-nipype.nii.gz'
dlicv.inputs.batch_size = 4
dlicv.inputs.nJobs = 1

# Create Apply Mask Node
maskImage = Node(MaskImageInterface.MaskImage(), name='maskImage')
maskImage.inputs.in_file = '/nichart/data/F1/2.16.840.1.114362.1.12066432.24920037488.604832115.605.168.nii.gz'
maskImage.inputs.out_file = '/nichart/data/F1/masked4.nii.gz'

# Create MUSE Node
muse = Node(DeepMRSegInterface.DeepMRSegInference(), name='muse')
muse.inputs.mdl_dir1 = '/nichart/models/MUSE/LPS'
muse.inputs.mdl_dir2 = '/nichart/models/MUSE/PSL'
muse.inputs.mdl_dir3 = '/nichart/models/MUSE/SLP'
muse.inputs.out_file = '/nichart/data/F1/muse-nipype.nii.gz'
muse.inputs.batch_size = 4
# muse.inputs.nJobs = 1

# Initiation of a workflow
wf = Workflow(name="structural", base_dir="/nichart/working_dir")
wf.connect(dlicv, "out_file", maskImage, "mask_file")
wf.connect(maskImage, "out_file", muse, "in_file")

wf.base_dir = "/nichart/working_dir"
wf.run()