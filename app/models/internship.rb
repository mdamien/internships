class Internship < ActiveRecord::Base
  scope :from_year, -> (year) { where("year >= ?", year) }
  scope :to_year, -> (year) { where("year <= ?", year) }

  def self.order_internships(internships)
    return internships
               .order(year: :DESC)
               .order(semester: :DESC)
               .order(country: :ASC)
               .order(company: :ASC)
  end

  def self.most_recent_internships
    most_recent_year = Internship.maximum("year")
    return order_internships(Internship.from_year(most_recent_year))
  end

  def self.search query
    if query.has_key?(:from_year) && query.has_key?(:to_year) && query.has_key?(:from_semester) && query.has_key?(:to_semester) && query.has_key?(:internship_type) && query.has_key?(:branch)
      internships = from_year(query[:from_year]).to_year(query[:to_year])

      if query[:from_semester] == 'A'
        #Removing spring internship of from_year.
        internships = internships.where.not("semester LIKE '%P%' and year = ?", query[:from_year])
      end
      if query[:to_semester] == 'P'
        #Removing fall internship of from_year.
        internships = internships.where.not("semester LIKE '%A%' and year = ?", query[:to_year])
      end

      case query[:internship_type]
        when "tn05"
          internships = internships.where("level LIKE '%ouvrier%'")
        when "tn09"
         internships = internships.where("level LIKE '%assistant%'")
        when "tn10"
          internships = internships.where("level LIKE '%projet de fin%'")
        when "intercultural"
          internships = internships.where("level LIKE '%interculturel%'")
        when "apprenticeship"
          internships = internships.where("level LIKE '%apprentissage%'")
      end

      # Branch filter if internship type is not tn05 or not all internships.
      branch = Internship.all_branches[query[:branch]]
      if !branch.nil? && branch.has_key?("search") && (query[:internship_type] != "tn05" || query[:internship_type] != "all")
        internships = internships.where("branch LIKE ?", "%"+ branch["search"] + "%")
      end

      return order_internships(internships)
    end

    # Returning most recent internships if missing parameters.
    return most_recent_internships
  end

  def self.all_internship_years
    return select(:year).distinct.order(year: :ASC)
  end

  def self.internship_types
    return {
        "Tous" => "all",
        "TN05" => "tn05",
        "TN09" => "tn09",
        "TN10" => "tn10",
        "Apprentissage" => "apprenticeship",
        "Interculturel" => "intercultural"
    }
  end

  def self.all_branches
    return {
        "all" => {
            "name" => "Toutes"
        },
        "gb" => {
            "name" => "GB",
            "search" => "Biologique"
        },
        "gi" => {
            "name" => "GI",
            "search" => "Informatique"
        },
        "gm" => {
            "name" => "GM",
            "search" => "Génie Mécanique"
        },
        "gp" => {
            "name" => "GP",
            "search" => "des Procédés"
        },
        "gsm" => {
            "name" => "GSM",
            "search" => "Systèmes Mécaniques"
        },
        "gsu" => {
            "name" => "GSU",
            "search" => "Urbains"
        }
    }
  end
end