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
  
    1) Εκτελέστε αυτήν την εντολή για να κάνετε λήψη της τρέχουσας σταθερής έκδοσης του Docker Compose:
    
      * `sudo curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
    
    2) Εφαρμογή εκτελέσιμων δικαιωμάτων στο binary:
    
      * `sudo chmod +x /usr/local/bin/docker-compose`
