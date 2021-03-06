Rails.application.routes.draw do

  root 'application#index'

  get 'analytics' => 'analytics#index'
  get 'analytics/top-companies' => 'analytics#top_companies'
  get 'analytics/count-by-semester-request' => 'analytics#count_by_semester_request', :constraints => {:format => /(json)/}
  get 'analytics/top-companies-request' => 'analytics#top_companies_request', :constraints => { :format => /(json)/ }

  get 'application/:id' => 'application#view'
  get 'internships/:id' => 'internships#show', :id => /\d+/, :constraints => {:format => /(json)/}
  get 'internships/search' => 'internships#search_internships', :constraints => {:format => /(json)/}

  #Login routes
  get 'logout' => 'application#logout'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end