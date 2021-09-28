from os import listdir
from os.path import isfile, join, basename

output_filename = "gallery_a.html"
input_images_path = "../renders"

onlyfiles = [f for f in listdir(input_images_path) if isfile(join(input_images_path, f))]


htmlstr = '''
<!DOCTYPE html>
<html>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&family=Roboto:wght@100;300;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="gallery_a.css">

</head>
<body>

<!-- Header -->
<div class="header">
  <h1>SKY130_FD_SC_HD</h1>
  <p>SKY130 High Density Digital Standard Cells</p>
</div>


<!-- Modal Image PopUp -->
<div id="imageDetailPopUp" class="modal">
  <!-- The Close Button -->
  <span class="closeImagePopUp">&times;</span>

   <img class="modal-content" id="imgInPopup">

  <!-- Modal Caption (Image Text) -->
  <div id="caption"></div>
</div>
<script src="gallery_a.js"></script>



<!-- Photo Grid -->
<div class="row"> 
'''
onlyfiles.sort()

i = 0
for file in onlyfiles:
    if(i%4==0):
        htmlstr += '''
        <div class="column">
        '''

    cell_title = basename(file).split(".")[0]
    cell_title = cell_title.replace("sky130_fd_sc_hd__","")
    cell_title = cell_title.replace("_TOP","")
    cell_title = cell_title.replace("_PERSPECTIVE","")
    

    htmlstr += '    <img src="../renders/' + basename(file) + '" style="width:100%" onclick="openImage(this)" alt="' + cell_title + '">'
    # htmlstr += '    <a href="../renders/'+ basename(file) +'" target="_blank"><img src="../renders/' + basename(file) + '" style="width:100%" alt="' + cell_title + '"></a>'
    if(i%2==1):
        
        htmlstr += '<br>' + cell_title + '<br><br>'

    i = i + 1
    if(i%4==0):
        htmlstr += '''
        </div>
        '''

htmlstr += '''
</div>




</body>
</html>
'''

outputf = open(output_filename, "w")
outputf.write(htmlstr)
outputf.close()


# print(list(onlyfiles))