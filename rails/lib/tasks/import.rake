require 'csv'

namespace :app do
  desc "Import internships from csv file"
  
  task :import, [:file] => [:environment] do |t,args|
    file = args[:file]

    Internship.delete_all

    #addresse,branche,branche_abbrev,city,company,confidentiel,country,description,done,etudiant,filiere,filiere_abbrev,lat,lng,niveau,niveau_abbrev,num,semestre,semestre_annee,semestre_trimestre,sujet,tuteur
    CSV.foreach(file, :headers => true) do |row|

      if Internship.where(:id => row[16]).blank?
        Internship.create({
          address: row[0],
          branch: row[1],
          branch_abbreviation: row[2],
          city: row[3],
          company: row[4],
          confidential: row[5] == "x" ? true : false,
          country: row[6],
          description: row[7],
          done: row[8] == "x" ? true : false,
          student: row[9],
          filiere: row[10],
          filiere_abbreviation: row[11],
          latitude: row[12],
          longitude: row[13],
          level: row[14],
          level_abbreviation: row[15],
          id: row[16],
          year: row[18],
          semester: row[19],
          subject: row[20],
          teacher: row[21]
        })
      else
        puts row[16].inspect
      end
    end
  end

  task :import_fake_data, [:file] => [:environment] do |t,args|
    file = args[:file]

    Internship.delete_all

    #num,addresse,branche_abbrev,filiere,company,description,etudiant,niveau,semestre,semestre_annee,sujet,tuteur,done,confidentiel,country,city,lat,lng
    CSV.foreach(file, :headers => true) do |row|
      Internship.create({
        id: row[0],
        address: row[1],
        branch_abbreviation: row[2],
        filiere: row[3],
        company: row[4],
        description: row[5],
        student: row[6],
        level_abbreviation: row[7],
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