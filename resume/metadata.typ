// NOTICE: Copy this file to your root folder.

/* Personal Information */
#let firstName = "James"

#let lastName = "E. T. Smith, Ph.D."

#let personalInfo = (
  github: "jamesETsmith",
  phone: "+1 508 596 7110",
  email: "james.smith9113@gmail.com",
  linkedin: "james-smith-ph-d-8525792b",
  //custom-1: (icon: "", text: "example", link: "https://example.com"),
  //gitlab: "mintyfrankie",
  homepage: "jamesetsmith.github.io/",
  // orcid: "0000-0002-5130-8633",
  //researchgate: "John-Doe",
  //extraInfo: "",
)


/* Language-specific */
// Add your own languages while the keys must match the varLanguage variable
#let headerQuoteInternational = (
  "en": [Software engineer with experience in high performance computing, numerical linear algebra, and quantum chemistry, looking to work at the intersection of research and engineering teams.],
)

#let cvFooterInternational = (
  "en": "",
)

#let letterFooterInternational = (
  "": "Cover Letter",
  "en": "Cover Letter",
  "fr": "Lettre de motivation",
  "zh": "申请信"
)

#let nonLatinOverwriteInfo = (
  "customFont": "Heiti SC",
  "firstName": "王道尔",
  "lastName": "",
  // submit an issue if you think other variables should be in this array
)

/* Layout Setting */
#let awesomeColor = "skyblue" // Optional: skyblue, red, nephritis, concrete, darknight

#let profilePhoto = "headshot_smaller.png" // Leave blank if profil photo is not needed

#let varLanguage = "en" // INFO: value must matches folder suffix; i.e "zh" -> "./modules_zh"

#let varEntrySocietyFirst = false // Decide if you want to put your company in bold or your position in bold

#let varDisplayLogo = true // Decide if you want to display organisation logo or not
