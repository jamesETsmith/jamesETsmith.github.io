#import "template.typ": *
#show: layout

#cvHeader(hasPhoto: true, align: left)
  #autoImport("skills")
  #autoImport("professional")
  #autoImport("education") 
  #autoImport("volunteer")
  #autoImport("certificates")

  // #autoImport("projects")
  // #autoImport("publications")
#cvFooter()