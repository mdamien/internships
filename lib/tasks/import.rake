require 'csv'

namespace :app do
  desc "Import internships from csv file"
  
  task :import, [:file] => [:environment] do |t,args|
    file = args[:file]

    Internship.delete_all

    #num,addresse,branche_abbrev,filiere,company,description,etudiant,niveau,semestre,semestre_annee,sujet,tuteur,done,confidentiel,country,city,lat,lng
    CSV.foreach(file, :headers => true) do |row|
      Internship.create({
        id: row[0],
        address: row[1],
        branch: row[2],
        filiere: row[3],
        company: row[4],
        description: row[5],
        student: row[6],
        level: row[7],
        semester: row[8],
        year: row[9],
        subject: row[10],
        teacher: row[11],
        done: row[12] == "x" ? true : false,
        confidential: row[13] == "x" ? true : false,
        country: row[14],
        city: row[15],
        latitude: row[16],
        longitude: row[17]
      })
    end
  end
end