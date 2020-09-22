# InfoCinemas2020_E16120_Theodoros_Rokas

## Docker 

#### Εγκατάσταση Docker 
##### Απαιτήσεις συστήματος: 
__Hardware__:
* 64-bit processor με Second Level Address Translation (SLAT)
* 4GB system RAM
* BIOS-level hardware virtualization support πρέπει να είναι ενεργοποιημένο στις ρυθμίσεις του BIOS (συνήθως είναι ήδη activated)

__Εγκατάσταση στα Windows__: 
* Πρέπει να έχετε Windows 10 Pro, Windows 10 Student edition - Σε Windows Home δεν θα μπορέσει να γίνει εγκατάσταση σωστά
* Πρέπει επίσης να είναι ενεργοποιημένα τα: 
  * Hyper-V 
  * Containers Windows Features
* Κατεβάζετε το εκτελέσιμο αρχείο από εδώ: https://hub.docker.com/editions/community/docker-ce-desktop-wind
ows

__Εγκατάσταση στα Linux (Ubuntu)__:
* Αρκεί να εκτελέσετε τις παρακάτω εντολές στο terminal: 
  * `sudo apt-get update`
  * `sudo apt install -y apt-transport-https ca-certificates curl software-properties-common`
  * `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`
  * `sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"`
  * `sudo apt-get update`
  * `sudo apt install docker-ce`
  
## Docker Compose
  
#### Εγκατάσταση Docker Compose
##### Απαιτήσεις συστήματος: 
Το Docker Compose βασίζεται στο Docker Engine για οποιαδήποτε σημαντική εργασία, οπότε βεβαιωθείτε ότι έχετε εγκαταστήσει το Docker Engine τοπικά ή απομακρυσμένα
* Σε εφαρμογές όπως το Docker Desktop για Mac και Windows, το Docker Compose περιλαμβάνεται ως μέρος αυτών των εγκαταστάσεων.
* Σε συστήματα Linux, εγκαταστήστε πρώτα το Docker Engine για το λειτουργικό σας σύστημα όπως περιγράφεται στη σελίδα Get Docker και μετά επιστρέψτε εδώ για οδηγίες σχετικά με την εγκατάσταση σε συστήματα Linux.
  
__Εγκατάσταση στα Windows και Mac__:
* Το Docker Desktop για Windows/Mac και το Docker Toolbox περιλαμβάνουν ήδη το Compose μαζί με άλλες εφαρμογές Docker, οπότε οι χρήστες Windows/Mac δεν χρειάζεται να εγκαταστήσουν το Compose ξεχωριστά.
  
__Εγκατάσταση στα Linux__:
* Στο Linux, μπορείτε να κατεβάσετε το Docker Compose binary από τη σελίδα κυκλοφορίας του Compose repository στο GitHub. Ακολουθήστε τις οδηγίες από το σύνδεσμο, ο οποίος περιλαμβάνει την εκτέλεση της εντολής curl στο τερματικό σας για λήψη των binary αρχείων

Εκτελέστε αυτήν την εντολή για να κάνετε λήψη της τρέχουσας σταθερής έκδοσης του Docker Compose:
* `sudo curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

Εφαρμογή εκτελέσιμων δικαιωμάτων στο binary:    
* `sudo chmod +x /usr/local/bin/docker-compose`

## InfoCinemas
Εκτελέστε αυτήν την εντολή έτσι ώστε το Docker να δημιουργήσει μια containerized εκδοχή της εφαρμογής μας που θα αλληλεπιδρά με την Mongodb:
* `sudo docker-compose up -d`
 
Αφού περιμένετε λίγη ώρα προκειμένου το Docker να κατεβάσει τα images και να δημιουργήσει τα container, είστασε έτοιμοι να περιηγηθείτε στην εφαρμογή
#### Δυνατότητες απλού χρήστη
##### Main Page (0.0.0.0:5000/):
Η main σελίδα της εφαρμογής μας
 
##### Insert User (0.0.0.0:5000/insertuser)
Σε αυτήν την σελιδα ένας χρήστης εκχωρώντας τα στοιχεία του μπορεί να εγγραφεί στο σύστημα, με την προυπόθεση ότι το email που θα χρησιμοποιήσει θα είναι διαθέσιμο. Ζητούνται από τον χρήστη name, password, email 
 
##### Connect User (0.0.0.0:5000/connectuser)
Σε αυτήν την σελίδα ένας χρήστης εκχωρώντας σωστά στοιχεία μπορεί να συνδεθεί στο σύστημα, εφόσον είναι εγγεγραμένος και να αποκτήσει επιπλέον δυνατότητες. Ζητούνται email, password
 
##### Search Movie (0.0.0.0:5000/name@gmail.com/searchmovie/title of movie)
Σε αυτήν την σελίδα ένας χρήστης μπορεί να δει τα στοιχεία της ταινίας που αναζήτησε, αν αυτή υπάρχει και να αγοράσει εισητηρια τις αντιστοιχες μέρες που η ταινία προβάλλεται. Ζητούνται screening, tickets. Σε περίπτωση που υπάρχουν παραπάνω απο μια ταινίες με το ίδιο όνομα εμφανίζει την νεότερη
 
##### Show History (0.0.0.0:5000/name@gmail.com/showhistory)
Σε αυτήν την σελίδα ένας χρήστης μπορεί να δει το ιστορικό των ταινιών που έχει παρακολουθήσει, δηλαδή αυτών που έχει αγοράσει εισητήρια
 
#### Δυνατότητες διαχειριστή 
##### Insert Movie (0.0.0.0:5000/name@gmail.com/insertmovie)
Σε αυτήν την σελίδα ένας διαχειριστής μπορεί να εκχωρήσει μια ταινία στο σύστημα συμπληρώνοντας τα στοιχεία της. Ζητούνται title, year, description, screening (στη μορφη πχ "Monday, Wednesday, Friday" λόγω parsing κάθε φορά που υπάρχει ", ")
 
##### Update Movie (0.0.0.0:5000/name@gmail.com/updatemovie/title of movie)
Σε αυτήν την σελίδα ένας διαχειριστής μπορεί να ανανεώσει τα στοιχεία της ταινίας που αναζήτησε συμπληρώνοντας τις αλλαγές που θέλει να κάνει. Ζητούνται title, year, description, screening (στη μορφη πχ "Monday, Wednesday, Friday" λόγω parsing κάθε φορά που υπάρχει ", "). Σε περίπτωση που υπάρχουν παραπάνω απο μια ταινίες με το ίδιο όνομα ανανεώνει την παλαιότερη 
 
##### Delete Movie (0.0.0.0:5000/name@gmail.com/deletemovie/title of movie)
Σε αυτήν την σελίδα ένας διαχειριστής μπορεί να διαγράψει την ταινία που αναζήτησε απο το σύστημα. Σε περίπτωση που υπάρχουν παραπάνω απο μια ταινίες με το ίδιο όνομα διαγράφει την παλαιότερη 
 
##### Make Admin (0.0.0.0:5000/name@gmail.com/makeadmin)
Σε αυτήν την σελίδα ένας διαχειριστής μπορεί να κάνει έναν άλλον απλό χρήστη διαχειριστή εκχωρώντας τα στοιχεία του άλλου. Ζητούνται email, password

Εκτελέστε αυτήν την εντολή έτσι ώστε το Docker να σταματήσει τα container και επομένως την εφαρμογή: 
* `sudo docker-compose down`
